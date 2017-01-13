import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.match_related_core_factories import MatchFactory, MatchStadiumStatisticsFactory, \
    StadiumStandStatisticsFactory, StadiumLevelFactory, StadiumLevelItemFactory
from core.factories.matchday_related_core_factories import MatchdayFactory
from users.models import OFMUser


class OFMStadiumStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()

        self.user = OFMUser.objects.create_user(username='alice', password='alice')
        self.client.login(username='alice', password='alice')

        self.match = MatchFactory.create(user=self.user)

        self.stadium_stat = MatchStadiumStatisticsFactory.create(match=self.match)
        StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='N')
        StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='S')
        StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='W')
        StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='O')

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('seasons' in response.context_data)
        self.assertEqual(response.context_data['slider_min'], 50)
        self.assertEqual(response.context_data['slider_max'], 50)
        self.assertEqual(response.context_data['tolerance'], 5)
        self.assertTrue('stadium_configurations' in response.context_data)

    def test_user_can_see_his_latest_stadium_statistics_when_given_no_season(self):
        match2 = MatchFactory.create(
            user=self.user,
            home_team_statistics__strength=150,
            guest_team_statistics__strength=150
        )
        stadium_stat = MatchStadiumStatisticsFactory.create(match=match2)
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat, sector='N')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat, sector='S')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat, sector='W')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat, sector='O')
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'))
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(returned_json_data), 1)

        self.assertEqual(returned_json_data[0]['visitors'], 168)
        self.assertEqual(returned_json_data[0]['capacity'], 400)

    def test_user_can_only_see_his_stadium_statistics(self):
        user2 = OFMUser.objects.create_user(username='bob', password='bob')
        MatchFactory.create(user=user2, venue='woanders')

        options = {
            'harmonic_strength': 50,
            'tolerance': 2,
        }

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'), options)
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(returned_json_data), 1)

        self.assertEqual(returned_json_data[0]['visitors'], 168)
        self.assertEqual(returned_json_data[0]['capacity'], 400)
        self.assertEqual(returned_json_data[0]['venue'], self.match.venue)

    def test_get_two_different_matches_with_same_harmonic_strength(self):
        match2 = MatchFactory.create(
            user=self.user,
            home_team_statistics__strength=30,
            guest_team_statistics__strength=150
        )
        MatchStadiumStatisticsFactory.create(match=match2)

        options = {
            'harmonic_strength': 50,
            'tolerance': 2,
        }

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'), options)
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(returned_json_data), 2)

        self.assertEqual(returned_json_data[0]['home_strength'], 50)
        self.assertEqual(returned_json_data[0]['guest_strength'], 50)
        self.assertEqual(str(returned_json_data[0]['harmonic_strength'])[:2], '50')
        self.assertEqual(returned_json_data[1]['home_strength'], 30)
        self.assertEqual(returned_json_data[1]['guest_strength'], 150)
        self.assertEqual(str(returned_json_data[1]['harmonic_strength'])[:2], '50')

    def test_user_can_narrow_statistics_with_strength_slider_by_cookie(self):
        cookies = self.client.cookies
        cookies['slider_min'] = 50
        cookies['slider_max'] = 50
        cookies['tolerance'] = 0

        options = {
            'harmonic_strength': 50,
            'tolerance': 2,
        }

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'), options)
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(returned_json_data), 1)

        self.assertEqual(returned_json_data[0]['visitors'], 168)
        self.assertEqual(returned_json_data[0]['capacity'], 400)
        self.assertEqual(returned_json_data[0]['home_strength'], 50)
        self.assertEqual(returned_json_data[0]['guest_strength'], 50)
        self.assertEqual(str(returned_json_data[0]['harmonic_strength'])[:2], '50')
        self.assertEqual(returned_json_data[0]['venue'], self.match.venue)

    def test_default_values_from_last_match_for_strength_slider(self):
        matchday = MatchdayFactory.create(number=2)
        match2 = MatchFactory.create(
            user=self.user,
            home_team_statistics__strength=30,
            guest_team_statistics__strength=150,
            matchday=matchday
        )
        MatchStadiumStatisticsFactory.create(match=match2)

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['slider_min'], 30)
        self.assertEqual(response.context_data['slider_max'], 150)
        self.assertEqual(response.context_data['tolerance'], 5)

    def test_default_values_from_cookies_for_strength_slider(self):
        cookies = self.client.cookies
        cookies['slider_min'] = 13
        cookies['slider_max'] = 37
        cookies['tolerance'] = 42
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['slider_min'], 13)
        self.assertEqual(response.context_data['slider_max'], 37)
        self.assertEqual(response.context_data['tolerance'], 42)

    def test_user_can_filter_for_stadium_configuration(self):
        matchday = MatchdayFactory.create(number=2)
        match2 = MatchFactory.create(user=self.user, matchday=matchday)
        light_level = StadiumLevelItemFactory(current_level=1)
        level = StadiumLevelFactory.create(light=light_level)
        stadium_stat_2 = MatchStadiumStatisticsFactory.create(match=match2, level=level)
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat_2, sector='N')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat_2, sector='S')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat_2, sector='W')
        StadiumStandStatisticsFactory.create(stadium_statistics=stadium_stat_2, sector='O')

        options = {
            'harmonic_strength': 50,
            'tolerance': 2,
            'configuration_filter': self.stadium_stat.get_configuration()
        }
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'), options)
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(returned_json_data), 1)
