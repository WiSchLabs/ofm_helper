import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Checklist, ChecklistItem
from users.models import OFMUser


class ChecklistSettingsTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user('temporary', 'temporary@ofmhelper.com', 'temporary', ofm_username="tmp", ofm_password="temp")
        self.checklist = Checklist.objects.create(user=self.user)
        self.checklist_item = ChecklistItem.objects.create(checklist=self.checklist, name='do more unit tests')
        self.user2 = OFMUser.objects.create_user('second', 'second@ofmhelper.com', 'second', ofm_username="second", ofm_password="second")
        checklist2 = Checklist.objects.create(user=self.user2)
        ChecklistItem.objects.create(checklist=checklist2, name='do less unit tests')
        self.matchday = MatchdayFactory.create(number=7)

    def test_get_checklist_items(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(returned_json_data), 1)
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['name'], 'do more unit tests')

    def test_create_standard_checklist_item(self):
        self.client.login(username='second', password='second')
        response = self.client.get(reverse('core:settings_add_checklist_item'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data)
        self.assertTrue('name' in returned_json_data)
        self.assertNotEqual(returned_json_data['name'], 'do more unit tests')
        self.assertNotEqual(returned_json_data['name'], 'do less unit tests')

    def test_update_checklist_item_name(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_name': 'do even more unit tests'
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['name'], 'do even more unit tests')
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).name, 'do even more unit tests')

    def test_update_checklist_item_home_match(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_home_match': True
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertFalse('type_matchday' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertTrue('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_home_match'], True)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, True)

    def test_update_checklist_item_matchday(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_matchday': 4
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('type_matchday' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_matchday'], 4)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday, 4)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, False)

    def test_update_checklist_item_matchday_pattern(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_matchday_pattern': 2
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertFalse('type_matchday' in returned_json_data[0])
        self.assertTrue('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_matchday_pattern'], 2)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, 2)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, False)

    def test_update_checklist_item_everyday(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_everyday': True
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertFalse('type_matchday' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, False)

    def test_update_checklist_item_checked(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_checked': True
                                     })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).last_checked_on_matchday, self.matchday)

    def test_delete_checklist_item(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_delete_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(returned_json_data), 0)
