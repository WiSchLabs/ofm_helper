import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.models import ParsingSetting
from users.models import OFMUser


class SettingsViewsTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user(
            username='temporary',
            email='temporary@ofmhelper.com',
            password='temporary',
            ofm_username="tmp",
            ofm_password="temp"
        )
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = True
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        self.client.login(username='temporary', password='temporary')

    def test_get_parsing_settings(self):
        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], True)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], True)
        self.assertEqual(returned_json_data['parsing_stadium_details'], True)

    def test_update_parsing_settings_disable_awp(self):
        response = self.client.post(reverse('core:account:update_parsing_setting_item_status'),
                                    {'parsing_awp_boundaries': 'false'})
        self.assertEqual(response.status_code, 200)

        parsing_setting = ParsingSetting.objects.get(user=self.user)
        self.assertTrue(parsing_setting.parsing_chain_includes_player_statistics)
        self.assertFalse(parsing_setting.parsing_chain_includes_awp_boundaries)
        self.assertTrue(parsing_setting.parsing_chain_includes_finances)
        self.assertTrue(parsing_setting.parsing_chain_includes_matches)
        self.assertTrue(parsing_setting.parsing_chain_includes_match_details)
        self.assertTrue(parsing_setting.parsing_chain_includes_stadium_details)

        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], False)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], True)
        self.assertEqual(returned_json_data['parsing_stadium_details'], True)

    def test_update_parsing_settings_disable_match_details(self):
        response = self.client.post(reverse('core:account:update_parsing_setting_item_status'),
                                    {'parsing_match_details': 'false'})
        self.assertEqual(response.status_code, 200)

        parsing_setting = ParsingSetting.objects.get(user=self.user)
        self.assertTrue(parsing_setting.parsing_chain_includes_player_statistics)
        self.assertTrue(parsing_setting.parsing_chain_includes_awp_boundaries)
        self.assertTrue(parsing_setting.parsing_chain_includes_finances)
        self.assertTrue(parsing_setting.parsing_chain_includes_matches)
        self.assertFalse(parsing_setting.parsing_chain_includes_match_details)
        self.assertFalse(parsing_setting.parsing_chain_includes_stadium_details)

        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], True)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], False)
        self.assertEqual(returned_json_data['parsing_stadium_details'], False)

    def test_update_parsing_settings_disable_matches(self):
        response = self.client.post(reverse('core:account:update_parsing_setting_item_status'),
                                    {'parsing_matches': 'false'})
        self.assertEqual(response.status_code, 200)

        parsing_setting = ParsingSetting.objects.get(user=self.user)
        self.assertTrue(parsing_setting.parsing_chain_includes_player_statistics)
        self.assertTrue(parsing_setting.parsing_chain_includes_awp_boundaries)
        self.assertTrue(parsing_setting.parsing_chain_includes_finances)
        self.assertFalse(parsing_setting.parsing_chain_includes_matches)
        self.assertFalse(parsing_setting.parsing_chain_includes_match_details)
        self.assertFalse(parsing_setting.parsing_chain_includes_stadium_details)

        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], True)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], False)
        self.assertEqual(returned_json_data['parsing_match_details'], False)
        self.assertEqual(returned_json_data['parsing_stadium_details'], False)

    def test_update_parsing_settings_enable_matches(self):
        parsing_setting = ParsingSetting.objects.get(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = False
        parsing_setting.parsing_chain_includes_match_details = False
        parsing_setting.parsing_chain_includes_stadium_details = False
        parsing_setting.save()
        response = self.client.post(reverse('core:account:update_parsing_setting_item_status'),
                                    {'parsing_matches': 'true'})
        self.assertEqual(response.status_code, 200)

        parsing_setting = ParsingSetting.objects.get(user=self.user)
        self.assertTrue(parsing_setting.parsing_chain_includes_player_statistics)
        self.assertTrue(parsing_setting.parsing_chain_includes_awp_boundaries)
        self.assertTrue(parsing_setting.parsing_chain_includes_finances)
        self.assertTrue(parsing_setting.parsing_chain_includes_matches)
        self.assertFalse(parsing_setting.parsing_chain_includes_match_details)
        self.assertFalse(parsing_setting.parsing_chain_includes_stadium_details)

        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], True)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], False)
        self.assertEqual(returned_json_data['parsing_stadium_details'], False)
