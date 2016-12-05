import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, MatchFactory, \
    MatchStadiumStatisticsFactory, StadiumStandStatisticsFactory
from users.models import OFMUser


class OFMStadiumStandStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()
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
        response = self.client.get('/ofm/stadium_stand/?sector=N')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('seasons' in response.context_data)
        self.assertTrue('sectors' in response.context_data)
        self.assertTrue('season' in response.context_data)
        self.assertTrue('sector_name' in response.context_data)
        self.assertEqual(response.context_data['sector_name'], 'Nord')

    def test_user_cannot_see_other_users_data(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/stadium_stand/?sector=N')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('sector_name' in response.context_data)

    def test_finance_balance_chart_json(self):
        response = self.client.get(reverse('core:ofm:stadium_stand_statistics_chart_json'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)
        self.assertEquals('Kapazität', returned_json_data['series'][0]['name'])
        self.assertEquals('Zuschauer', returned_json_data['series'][1]['name'])
        self.assertEquals('Ticketpreis', returned_json_data['series'][2]['name'])
        self.assertEquals('Zustand', returned_json_data['series'][3]['name'])
        self.assertEquals('Gemittelte Stärke der Mannschaften', returned_json_data['series'][4]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])
        self.assertTrue('categories' in returned_json_data)
        self.assertTrue('yAxis' in returned_json_data)


