import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, ChecklistItemFactory, ChecklistFactory, MatchFactory, \
    FinanceFactory
from core.models import ChecklistItem
from users.models import OFMUser


class ChecklistSettingsTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user(
            username='temporary',
            email='temporary@ofmhelper.com',
            password='temporary',
            ofm_username="tmp",
            ofm_password="temp"
        )
        self.checklist = ChecklistFactory.create(user=self.user)
        self.checklist_item = ChecklistItemFactory.create(checklist=self.checklist, name='do more unit tests')
        self.user2 = OFMUser.objects.create_user(
            username='second',
            email='second@ofmhelper.com',
            password='second',
            ofm_username="second",
            ofm_password="second"
        )
        checklist2 = ChecklistFactory.create(user=self.user2)
        ChecklistItemFactory.create(checklist=checklist2, name='do less unit tests')
        self.matchday = MatchdayFactory.create(number=6)

    def test_get_checklist_items(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(returned_json_data), 1)
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('checked' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['name'], 'do more unit tests')
        self.assertEqual(returned_json_data[0]['checked'], False)

    def test_create_standard_checklist_item(self):
        self.client.login(username='second', password='second')
        response = self.client.get(reverse('core:settings_add_checklist_item'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data)
        self.assertTrue('name' in returned_json_data)
        self.assertTrue('checked' in returned_json_data)
        self.assertNotEqual(returned_json_data['name'], 'do more unit tests')
        self.assertNotEqual(returned_json_data['name'], 'do less unit tests')
        self.assertEqual(returned_json_data['checked'], False)

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
        self.assertFalse('type_matchdays' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertTrue('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_home_match'], True)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchdays, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, True)

    def test_update_checklist_item_matchday(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_matchdays': '4'
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('type_matchdays' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_matchdays'], '4')
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchdays, "4")
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, False)

    def test_update_checklist_item_matchdays(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_matchdays': '3,33'
                                     })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('type_matchdays' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_matchdays'], '3,33')
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchdays, "3,33")
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
        self.assertFalse('type_matchdays' in returned_json_data[0])
        self.assertTrue('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['type_matchday_pattern'], 2)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchdays, None)
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
        self.assertFalse('type_matchdays' in returned_json_data[0])
        self.assertFalse('type_matchday_pattern' in returned_json_data[0])
        self.assertFalse('type_home_match' in returned_json_data[0])
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchdays, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_on_matchday_pattern, None)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).to_be_checked_if_home_match_tomorrow, False)

    def test_update_checklist_item_checked(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_checked': 'true'
                                     })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).last_checked_on_matchday, self.matchday)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('checked' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['checked'], True)

    def test_update_checklist_item_unchecked(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:settings_update_checklist_item'),
                                    {'checklist_item_id': self.checklist_item.id,
                                     'checklist_item_checked': 'false'
                                     })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChecklistItem.objects.get(id=self.checklist_item.id).last_checked_on_matchday, None)

        response = self.client.get(reverse('core:settings_get_checklist_items'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in returned_json_data[0])
        self.assertTrue('name' in returned_json_data[0])
        self.assertTrue('checked' in returned_json_data[0])
        self.assertEqual(returned_json_data[0]['checked'], False)

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

    def test_get_checklist_items_for_today(self):
        self.client.login(username='temporary', password='temporary')
        c1 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on 4th matchday',
            to_be_checked_on_matchdays='4'
        )
        c2 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on every 4th matchday',
            to_be_checked_on_matchday_pattern=4
        )
        c3 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on every 3rd matchday',
            to_be_checked_on_matchday_pattern=3
        )
        c4 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='if tomorrow home_match',
            to_be_checked_if_home_match_tomorrow=True
        )
        c5 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on 6th matchday',
            to_be_checked_on_matchdays='6,9'
        )

        response = self.client.get(reverse('core:settings_get_checklist_items_for_today'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        returned_checklist_item_ids = [checklist_item['id'] for checklist_item in returned_json_data]
        self.assertTrue(self.checklist_item.id in returned_checklist_item_ids)
        self.assertTrue(c1.id not in returned_checklist_item_ids)
        self.assertTrue(c2.id not in returned_checklist_item_ids)
        self.assertTrue(c3.id in returned_checklist_item_ids)
        self.assertTrue(c4.id not in returned_checklist_item_ids)
        self.assertTrue(c5.id in returned_checklist_item_ids)

    def test_get_checklist_items_for_today_if_tomorrow_home_match(self):
        matchday2 = MatchdayFactory.create(number=7)
        FinanceFactory.create(matchday=self.matchday, user=self.user)
        MatchFactory.create(matchday=matchday2, venue='', is_home_match=True, user=self.user)
        self.client.login(username='temporary', password='temporary')
        c1 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on 6th and 9th matchday',
            to_be_checked_on_matchdays='6,9'
        )
        c2 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on every 2nd matchday',
            to_be_checked_on_matchday_pattern=2
        )
        c3 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='on every 9th matchday',
            to_be_checked_on_matchday_pattern=9
        )
        c4 = ChecklistItemFactory.create(
            checklist=self.checklist,
            name='if tomorrow home_match',
            to_be_checked_if_home_match_tomorrow=True
        )

        response = self.client.get(reverse('core:settings_get_checklist_items_for_today'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        returned_checklist_item_ids = [checklist_item['id'] for checklist_item in returned_json_data]
        self.assertTrue(self.checklist_item.id in returned_checklist_item_ids)
        self.assertTrue(c1.id in returned_checklist_item_ids)
        self.assertTrue(c2.id in returned_checklist_item_ids)
        self.assertTrue(c3.id not in returned_checklist_item_ids)
        self.assertTrue(c4.id in returned_checklist_item_ids)
