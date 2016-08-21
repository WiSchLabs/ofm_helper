import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, PlayerFactory
from core.models import Contract
from users.models import OFMUser


class OFMPlayerDetailViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        self.matchday = MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        Contract.objects.create(user=self.user1, player=self.player, bought_on_matchday=self.matchday, sold_on_matchday=None)
        self.client.login(username='alice', password='alice')

    def test_user_can_see_his_players(self):
        response = self.client.get('/ofm/players/'+str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('player' in response.context_data)
        self.assertTrue('seasons' in response.context_data)

    def test_user_cannot_see_other_users_players(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/players/'+str(self.player.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('player' in response.context_data)

    def test_player_chart_json(self):
        response = self.client.get(reverse('core:ofm:players_chart_json'), {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)
        self.assertEquals('AWP', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])
        self.assertTrue('categories' in returned_json_data)
