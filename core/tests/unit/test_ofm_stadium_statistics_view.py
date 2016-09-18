import json

from core.factories.core_factories import MatchdayFactory, MatchFactory, \
    MatchStadiumStatisticsFactory, StadiumStandStatisticsFactory
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMStadiumStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()

        self.user = OFMUser.objects.create_user(username='alice', password='alice')
        self.client.login(username='alice', password='alice')

        self.match = MatchFactory.create(user=self.user)

        self.stadium_stat = MatchStadiumStatisticsFactory.create(match=self.match)
        self.north_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='N')
        self.south_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='S')
        self.west_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='W')
        self.east_stand_stat = StadiumStandStatisticsFactory.create(stadium_statistics=self.stadium_stat, sector='O')

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('seasons' in response.context_data)

    def test_user_can_see_his_latest_stadium_statistics_when_given_no_season(self):
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'))
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(returned_json_data), 1)

        self.assertEquals(returned_json_data[0]['visitors'], 168)
        self.assertEquals(returned_json_data[0]['capacity'], 400)

    def test_user_can_only_see_only_his_latest_stadium_statistics(self):
        user2 = OFMUser.objects.create_user(username='bob', password='bob')
        MatchFactory.create(user=user2, venue='woanders')

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'))
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(returned_json_data), 1)

        self.assertEquals(returned_json_data[0]['visitors'], 168)
        self.assertEquals(returned_json_data[0]['capacity'], 400)
        self.assertEquals(returned_json_data[0]['venue'], self.match.venue)

    def test_get_two_different_matches_with_same_harmonic_strength(self):
        match2 = MatchFactory.create(user=self.user, home_team_statistics__strength=30, guest_team_statistics__strength=150)
        MatchStadiumStatisticsFactory.create(match=match2)

        options = {
            'harmonic_strength': 50,
            'tolerance': 2,
        }

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview_json'), options)
        returned_json_data = json.loads(response.content.decode('utf-8'))

        self.assertEquals(len(returned_json_data), 2)

        self.assertEquals(returned_json_data[0]['home_strength'], 50)
        self.assertEquals(returned_json_data[0]['guest_strength'], 50)
        self.assertEquals(returned_json_data[0]['harmonic_strength'], 50)
        self.assertEquals(returned_json_data[1]['home_strength'], 30)
        self.assertEquals(returned_json_data[1]['guest_strength'], 150)
        self.assertEquals(returned_json_data[1]['harmonic_strength'], 50)

    def test_default_values_from_last_match_for_strength_slider(self):
        matchday = MatchdayFactory.create(number=2)
        match2 = MatchFactory.create(user=self.user, home_team_statistics__strength=30, guest_team_statistics__strength=150, matchday=matchday)
        MatchStadiumStatisticsFactory.create(match=match2)

        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['slider_min'], 30)
        self.assertEqual(response.context_data['slider_max'], 150)

    def test_default_values_from_cookies_for_strength_slider(self):
        session = self.client.session
        session['slider_min'] = 13
        session['slider_max'] = 37
        session.save()
        response = self.client.get(reverse('core:ofm:stadium_statistics_overview'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['slider_min'], 13)
        self.assertEqual(response.context_data['slider_max'], 37)
