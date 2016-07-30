import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory
from core.models import Contract
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMPlayerStatisticsViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        self.matchday = MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice', ofm_password='alice')
        Contract.objects.create(user=self.user1, player=self.player, bought_on_matchday=self.matchday, sold_on_matchday=None)
        self.client.login(username='alice', password='alice')
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)

    def test_user_can_see_table(self):
        response = self.client.get(reverse('core:ofm:player_statistics'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_choose_between_matchdays(self):
        next_matchday = MatchdayFactory.create(number=1)
        PlayerStatisticsFactory.create(player=self.player, matchday=next_matchday, ep=3, tp=6, awp=4)

        response = self.client.get(reverse('core:ofm:player_statistics'))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(next_matchday, response.context_data['matchdays'][0])
        self.assertEquals(self.matchday, response.context_data['matchdays'][1])

    def test_user_can_see_his_latest_player_statistics_total_when_given_no_matchday(self):

        response = self.client.get(reverse('core:ofm:player_statistics_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 2)
        self.assertEquals(returned_json_data[0]['tp'], 5)
        self.assertEquals(returned_json_data[0]['awp'], 3)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 4)

    def test_user_can_see_his_player_statistics_diff_when_given_both_matchdays(self):
        second_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        PlayerStatisticsFactory.create(player=self.player, matchday=second_matchday, ep=3, tp=6, awp=4, freshness=5)

        third_matchday = MatchdayFactory.create(number=self.matchday.number+2)
        PlayerStatisticsFactory.create(player=self.player, matchday=third_matchday, ep=12, tp=15, awp=13, freshness=14)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                    })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 10)
        self.assertEquals(returned_json_data[0]['tp'], 10)
        self.assertEquals(returned_json_data[0]['awp'], 10)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 10)

    def test_user_can_see_his_player_statistics_diff_when_given_only_newer_matchday(self):
        second_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        PlayerStatisticsFactory.create(player=self.player, matchday=second_matchday, ep=3, tp=6, awp=4, freshness=5)

        third_matchday = MatchdayFactory.create(number=self.matchday.number+2)
        PlayerStatisticsFactory.create(player=self.player, matchday=third_matchday, ep=12, tp=15, awp=13, freshness=14)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number
                                   })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 12)
        self.assertEquals(returned_json_data[0]['tp'], 15)
        self.assertEquals(returned_json_data[0]['awp'], 13)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 14)

    def test_player_leaves_team_shows_only_older_player_data(self):
        second_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        player2 = PlayerFactory.create(name="Tricia McMillan")
        Contract.objects.create(user=self.user1, player=player2, bought_on_matchday=self.matchday, sold_on_matchday=None)

        PlayerStatisticsFactory.create(player=player2, matchday=self.matchday, ep=3, tp=6, awp=4, freshness=5)
        PlayerStatisticsFactory.create(player=self.player, matchday=second_matchday, ep=3, tp=6, awp=4, freshness=5)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': second_matchday.season.number,
                                    'newer_matchday': second_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                   })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], self.player.position)
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 1)
        self.assertEquals(returned_json_data[0]['tp'], 1)
        self.assertEquals(returned_json_data[0]['awp'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 1)

    def test_player_joins_team_shows_only_older_player_data(self):
        second_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        player2 = PlayerFactory.create(name="Tricia McMillan")
        Contract.objects.create(user=self.user1, player=player2, bought_on_matchday=self.matchday, sold_on_matchday=None)

        PlayerStatisticsFactory.create(player=player2, matchday=second_matchday, ep=3, tp=6, awp=4, freshness=5)
        PlayerStatisticsFactory.create(player=self.player, matchday=second_matchday, ep=3, tp=6, awp=4, freshness=5)

        response = self.client.get(reverse('core:ofm:player_statistics_json'),
                                   {'newer_matchday_season': second_matchday.season.number,
                                    'newer_matchday': second_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                   })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], self.player.position)
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 1)
        self.assertEquals(returned_json_data[0]['tp'], 1)
        self.assertEquals(returned_json_data[0]['awp'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 1)


