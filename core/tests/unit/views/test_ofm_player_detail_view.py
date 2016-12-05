import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory
from core.models import Contract, AwpBoundaries
from users.models import OFMUser


class OFMPlayerDetailViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        self.matchday = MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice',
                                                 ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob',
                                                 ofm_password='bob')
        Contract.objects.create(user=self.user1, player=self.player, bought_on_matchday=self.matchday,
                                sold_on_matchday=None)
        self.client.login(username='alice', password='alice')

    def test_user_can_see_his_players(self):
        PlayerStatisticsFactory.create(player=self.player)
        response = self.client.get('/ofm/players/' + str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('player' in response.context_data)
        self.assertTrue('player_age' in response.context_data)
        self.assertTrue('player_strength' in response.context_data)
        self.assertTrue('seasons' in response.context_data)

    def test_user_cannot_see_other_users_players(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/players/' + str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('player' in response.context_data)

    def test_player_chart_json(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 1000

        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)

        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])

        self.assertEquals('AWP-Grenze: 2', returned_json_data['series'][1]['name'])
        self.assertTrue('data' in returned_json_data['series'][1])
        self.assertEquals([1000], returned_json_data['series'][1]['data'])

        self.assertTrue('categories' in returned_json_data)

    def test_player_chart_shows_awp_boundaries_which_are_only_greater_than_my_strength(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday, strength=3, awp=3500)

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 2000
        awp_boundaries[3] = 3000
        awp_boundaries[4] = 4000

        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)

        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])

        self.assertEquals('AWP-Grenze: 4', returned_json_data['series'][1]['name'])
        self.assertTrue('data' in returned_json_data['series'][1])
        self.assertEquals([4000], returned_json_data['series'][1]['data'])

    def test_player_chart_shows_reached_but_not_promoted_awp_boundary(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday, strength=2, awp=2800)
        PlayerStatisticsFactory.create(player=self.player, matchday=MatchdayFactory.create(number=1), strength=2,
                                       awp=3500)

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 2000
        awp_boundaries[3] = 3000
        awp_boundaries[4] = 4000

        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)

        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])

        self.assertEquals('AWP-Grenze: 3', returned_json_data['series'][1]['name'])
        self.assertTrue('data' in returned_json_data['series'][1])
        self.assertEquals([3000] * 2, returned_json_data['series'][1]['data'])

        self.assertEquals('AWP-Grenze: 4', returned_json_data['series'][2]['name'])
        self.assertTrue('data' in returned_json_data['series'][2])
        self.assertEquals([4000] * 2, returned_json_data['series'][2]['data'])

    def test_player_chart_does_not_show_boundary_if_promoted(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday, strength=2, awp=2800)
        matchday_9 = MatchdayFactory.create(number=9)
        PlayerStatisticsFactory.create(player=self.player, matchday=matchday_9, strength=3, awp=3500)

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 2000
        awp_boundaries[3] = 3000
        awp_boundaries[4] = 3800
        awp_boundaries9 = AwpBoundaries.get_or_create_from_matchday(matchday_9)
        awp_boundaries9[2] = 2000
        awp_boundaries9[3] = 3000
        awp_boundaries9[4] = 4000

        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)

        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])

        self.assertEquals('AWP-Grenze: 4', returned_json_data['series'][1]['name'])
        self.assertTrue('data' in returned_json_data['series'][1])
        self.assertEquals([3800, 4000], returned_json_data['series'][1]['data'])

    def test_player_chart_shows_different_awp_boundaries(self):
        matchday_9 = MatchdayFactory.create(number=9)

        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        PlayerStatisticsFactory.create(player=self.player, matchday=matchday_9)

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 2000

        awp_boundaries_9 = AwpBoundaries.get_or_create_from_matchday(matchday_9)
        awp_boundaries_9[2] = 3000

        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)

        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])

        self.assertEquals('AWP-Grenze: 2', returned_json_data['series'][1]['name'])
        self.assertTrue('data' in returned_json_data['series'][1])
        self.assertEquals([2000, 3000], returned_json_data['series'][1]['data'])
