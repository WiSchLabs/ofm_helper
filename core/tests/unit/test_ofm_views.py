import json

from core.factories.core_factories import MatchdayFactory, PlayerFactory, PlayerStatisticsFactory
from core.models import Contract
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser


class OFMViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        self.matchday = MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        Contract.objects.create(user=self.user1, player=self.player, bought_on_matchday=self.matchday, sold_on_matchday=None)
        self.client.login(username='alice', password='alice')

    def test_user_can_see_his_player_list(self):
        response = self.client.get(reverse('core:ofm:player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['player_list']) > 0)

    def test_user_cannot_see_other_users_player_list(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get(reverse('core:ofm:player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(len(response.context_data['player_list']) > 0)

    def test_user_can_see_his_players(self):
        response = self.client.get('/ofm/players/'+str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('player' in response.context_data)

    def test_user_cannot_see_other_users_players(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/players/'+str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('player' in response.context_data)

    def test_user_can_see_table(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        response = self.client.get(reverse('core:ofm:player_data'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_player_statistics(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)

        response = self.client.get(reverse('core:ofm:player_data_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], 'Martin Adomeit')
        self.assertEquals(returned_json_data[0]['ep'], '2 ()')
        self.assertEquals(returned_json_data[0]['tp'], '5 ()')
        self.assertEquals(returned_json_data[0]['awp'], '3 ()')
        self.assertEquals(returned_json_data[0]['strength'], 1)

    def test_user_can_see_player_statistics_diff(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        next_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        PlayerStatisticsFactory.create(player=self.player, matchday=next_matchday, ep=3, tp=6, awp=4)

        response = self.client.get(reverse('core:ofm:player_data_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], 'Martin Adomeit')
        self.assertEquals(returned_json_data[0]['ep'], '3 (1)')
        self.assertEquals(returned_json_data[0]['tp'], '6 (1)')
        self.assertEquals(returned_json_data[0]['awp'], '4 (1)')
        self.assertEquals(returned_json_data[0]['strength'], 1)

    def test_user_can_only_see_his_player_statistic(self):
        PlayerStatisticsFactory.create(player=self.player, matchday=self.matchday)
        next_matchday = MatchdayFactory.create(number=self.matchday.number+1)
        player2 = PlayerFactory.create()
        PlayerStatisticsFactory.create(player=player2, matchday=next_matchday, ep=3, tp=6, awp=4)

        response = self.client.get(reverse('core:ofm:player_data_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['position'], 'TW')
        self.assertEquals(returned_json_data[0]['name'], 'Martin Adomeit')
        self.assertEquals(returned_json_data[0]['ep'], '2 ()')
        self.assertEquals(returned_json_data[0]['tp'], '5 ()')
        self.assertEquals(returned_json_data[0]['awp'], '3 ()')
        self.assertEquals(returned_json_data[0]['strength'], 1)

