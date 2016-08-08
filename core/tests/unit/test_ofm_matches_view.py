import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory, MatchFactory
from core.models import Contract
from django.core.urlresolvers import reverse
from django.test import TestCase
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
        self.assertTrue('matchdays' in response.context_data)

    def test_user_can_see_his_latest_matches_when_given_no_season(self):
        response = self.client.get(reverse('core:ofm:matches_overview_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)

        #self.assertEquals(returned_json_data[0]['home_team'], '1. SC Wedding')
        #self.assertEquals(returned_json_data[0]['guest_team'], 'BSC Wittenau')
        #self.assertEquals(returned_json_data[0]['home_goals'], 42)
        #self.assertEquals(returned_json_data[0]['guest_goals'], 0)
        self.assertEquals(returned_json_data[0]['venue'], 'Olympiastadion Berlin')


