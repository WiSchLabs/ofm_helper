import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
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
        self.client.login(username='temporary', password='temporary')

    def test_get_parsing_settings(self):
        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], True)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], False)
        self.assertEqual(returned_json_data['parsing_stadium_details'], False)

    def test_update_parsing_settings(self):
        response = self.client.post(reverse('core:account:update_parsing_setting_item_status'),
                                    {'parsing_awp_boundaries': False})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('core:account:get_parsing_settings'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['parsing_player_statistics'], True)
        self.assertEqual(returned_json_data['parsing_awp_boundaries'], False)
        self.assertEqual(returned_json_data['parsing_finances'], True)
        self.assertEqual(returned_json_data['parsing_matches'], True)
        self.assertEqual(returned_json_data['parsing_match_details'], False)
        self.assertEqual(returned_json_data['parsing_stadium_details'], False)
