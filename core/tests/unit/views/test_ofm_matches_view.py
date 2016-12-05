import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, MatchFactory
from users.models import OFMUser


class OFMMatchesViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()
        self.second_matchday = MatchdayFactory.create(number=1)
        self.user1 = OFMUser.objects.create_user(username='alice', email='alice@ofmhelper.com', password='alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        MatchFactory.create(user=self.user1)
        self.client.login(username='alice', password='alice')

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:matches_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('seasons' in response.context_data)

    def test_user_can_see_his_latest_matches_when_given_no_season(self):
        response = self.client.get(reverse('core:ofm:matches_overview_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(returned_json_data), 1)

        self.assertTrue('Springfield Isotopes' in returned_json_data[0]['home_team'])
        self.assertTrue('Springfield Isotopes' in returned_json_data[0]['guest_team'])
        self.assertTrue('0:0' in returned_json_data[0]['result'])
        self.assertTrue('Olympiastadion Berlin' in returned_json_data[0]['venue'])

    def test_user_can_see_matches_summary(self):
        response = self.client.get(reverse('core:ofm:matches_summary_json'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(0, returned_json_data['matches_won'])
        self.assertEqual(1, returned_json_data['matches_draw'])
        self.assertEqual(0, returned_json_data['matches_lost'])
