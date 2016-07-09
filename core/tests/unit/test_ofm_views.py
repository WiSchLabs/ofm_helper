from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, PlayerFactory
from core.models import PlayerUserOwnership
from users.models import OFMUser


class OFMViewTestCase(TestCase):
    def setUp(self):
        self.player = PlayerFactory.create()
        matchday = MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        PlayerUserOwnership.objects.create(user=self.user1, player=self.player, bought_on_matchday=matchday, sold_on_matchday=None)
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
