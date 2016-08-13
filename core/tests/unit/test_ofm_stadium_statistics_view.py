import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory, MatchFactory, \
    MatchStadiumStatisticsFactory, StadiumStandStatisticsFactory
from core.models import Contract
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMStadiumStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()
        self.second_matchday = MatchdayFactory.create(number=1)
        self.user1 = OFMUser.objects.create_user(username='alice', email='alice@ofmhelper.com', password='alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        self.match = MatchFactory.create(user=self.user1)
        self.stadium_stat = MatchStadiumStatisticsFactory.create(match=self.match)
        self.north_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='N')
        self.south_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='S')
        self.west_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='W')
        self.east_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='O')
        self.client.login(username='alice', password='alice')

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('seasons' in response.context_data)

    def test_user_can_see_his_latest_stadium_statistics_when_given_no_season(self):
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)

        self.assertEquals(returned_json_data[0]['visitors'], 168)
        self.assertEquals(returned_json_data[0]['capacity'], 400)


