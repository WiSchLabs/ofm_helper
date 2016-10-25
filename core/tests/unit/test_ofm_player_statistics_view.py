import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory
from core.models import Contract, AwpBoundaries
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMPlayerStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        self.matchday = MatchdayFactory.create()
        self.second_matchday = MatchdayFactory.create(number=1)
        self.user1 = OFMUser.objects.create_user(username='alice', email='alice@ofmhelper.com', password='alice', ofm_username='alice', ofm_password='alice')
        Contract.objects.create(user=self.user1, player=self.player, bought_on_matchday=self.matchday, sold_on_matchday=None)
        self.client.login(username='alice', password='alice')
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        PlayerStatisticsFactory.create(player=self.player, matchday=self.second_matchday, ep=3, tp=6, awp=4, freshness=5)

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:player_statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('matchdays' in response.context_data)

    def test_user_can_choose_between_matchdays(self):
        response = self.client.get(reverse('core:ofm:player_statistics'))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(self.second_matchday, response.context_data['matchdays'][0])
        self.assertEquals(self.matchday, response.context_data['matchdays'][1])

    def test_user_can_see_his_latest_player_statistics_total_when_given_no_matchday(self):
        response = self.client.get(reverse('core:ofm:player_statistics_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 3)
        self.assertEquals(returned_json_data[0]['tp'], 6)
        self.assertEquals(returned_json_data[0]['awp'], 4)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 5)

    def test_user_can_see_his_player_statistics_diff_when_given_both_matchdays(self):
        third_matchday = MatchdayFactory.create(number=self.matchday.number+2)
        PlayerStatisticsFactory.create(player=self.player, matchday=third_matchday, ep=12, tp=15, awp=13, freshness=14)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                    })

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 10)
        self.assertEquals(returned_json_data[0]['tp'], 10)
        self.assertEquals(returned_json_data[0]['awp'], 10)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 10)

    def test_user_can_see_his_player_statistics_diff_when_given_only_newer_matchday(self):
        third_matchday = MatchdayFactory.create(number=self.matchday.number+2)
        PlayerStatisticsFactory.create(player=self.player, matchday=third_matchday, ep=12, tp=15, awp=13, freshness=14)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number
                                   })

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 12)
        self.assertEquals(returned_json_data[0]['tp'], 15)
        self.assertEquals(returned_json_data[0]['awp'], 13)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 14)

    def test_user_can_see_players_diff_to_next_awp_boundary_given_no_matchday(self):

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 20

        response = self.client.get(reverse('core:ofm:player_statistics_json'))

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(returned_json_data[0]['awp_to_next_bound'], 16)

    def test_user_can_see_players_diff_to_next_awp_boundary_given_matchdays(self):

        awp_boundaries = AwpBoundaries.get_or_create_from_matchday(self.matchday)
        awp_boundaries[2] = 20

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': self.second_matchday.season.number,
                                    'newer_matchday': self.second_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                    })

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(returned_json_data[0]['awp_to_next_bound'], 16)

    def test_player_leaves_team_shows_only_older_player_data(self):
        player2 = PlayerFactory.create(name="Tricia McMillan")
        Contract.objects.create(user=self.user1, player=player2, bought_on_matchday=self.matchday, sold_on_matchday=self.matchday)
        PlayerStatisticsFactory.create(player=player2, matchday=self.matchday, ep=3, tp=6, awp=4, freshness=5)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': self.second_matchday.season.number,
                                    'newer_matchday': self.second_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                    })

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], self.player.position)
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 1)
        self.assertEquals(returned_json_data[0]['tp'], 1)
        self.assertEquals(returned_json_data[0]['awp'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 1)

    def test_player_joins_team_shows_only_older_player_data(self):
        player2 = PlayerFactory.create(name="Tricia McMillan")
        Contract.objects.create(user=self.user1, player=player2, bought_on_matchday=self.matchday, sold_on_matchday=None)

        PlayerStatisticsFactory.create(player=player2, matchday=self.second_matchday, ep=3, tp=6, awp=4, freshness=5)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': self.second_matchday.season.number,
                                    'newer_matchday': self.second_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                   })

        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], self.player.position)
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 1)
        self.assertEquals(returned_json_data[0]['tp'], 1)
        self.assertEquals(returned_json_data[0]['awp'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 1)
