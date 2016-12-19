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

    def test_get_current_matchday(self):
        MatchdayFactory.create()
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:ofm:get_current_matchday'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(returned_json_data['matchday_number'], 0)
        self.assertEqual(returned_json_data['season_number'], 1)
