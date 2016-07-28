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

    def test_user_can_see_table(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        response = self.client.get(reverse('core:ofm:player_statistics'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_player_statistics_total(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)

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

    def test_user_can_see_player_statistics_diff(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        next_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        PlayerStatisticsFactory.create(player=self.player, matchday=next_matchday, ep=3, tp=6, awp=4, freshness=5)

        response = self.client.get(reverse('core:ofm:player_statistics_json'), {'show_diff': 'true'})

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], '<a href="/ofm/players/1">Martin Adomeit</a>')
        self.assertEquals(returned_json_data[0]['ep'], 1)
        self.assertEquals(returned_json_data[0]['tp'], 1)
        self.assertEquals(returned_json_data[0]['awp'], 1)
        self.assertEquals(returned_json_data[0]['strength'], 1)
        self.assertEquals(returned_json_data[0]['freshness'], 1)

    def test_user_can_only_see_his_player_statistic(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        next_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        player2 = PlayerFactory.create()
        PlayerStatisticsFactory.create(player=player2, matchday=next_matchday, ep=3, tp=6, awp=4)

        response = self.client.get(reverse('core:ofm:player_statistics_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
