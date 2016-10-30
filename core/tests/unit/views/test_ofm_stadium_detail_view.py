import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory, MatchFactory, \
    MatchStadiumStatisticsFactory, StadiumStandStatisticsFactory
from core.models import Contract
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMStadiumDetailsViewTestCase(TestCase):
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

    def test_user_can_see_his_data(self):
        response = self.client.get('/ofm/stadium/'+str(self.stadium_stat.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('stadium_stat' in response.context_data)
        self.assertTrue('north_stand' in response.context_data)
        self.assertTrue('south_stand' in response.context_data)
        self.assertTrue('west_stand' in response.context_data)
        self.assertTrue('east_stand' in response.context_data)

    def test_user_cannot_see_other_users_data(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/stadium/'+str(self.stadium_stat.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('stadium_stat' in response.context_data)
        self.assertFalse('north_stand' in response.context_data)
        self.assertFalse('south_stand' in response.context_data)
        self.assertFalse('west_stand' in response.context_data)
        self.assertFalse('east_stand' in response.context_data)


