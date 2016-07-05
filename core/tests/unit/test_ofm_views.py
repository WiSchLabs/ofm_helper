import os

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class OFMViewTestCase(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'), encoding='utf8')
        MatchdayFactory.create()
        self.user1 = OFMUser.objects.create_user('alice', 'alice@ofmhelper.com', 'alice', ofm_username='alice', ofm_password='alice')
        self.user2 = OFMUser.objects.create_user('bob', 'bob@ofmhelper.com', 'bob', ofm_username='bob', ofm_password='bob')
        self.client.login(username='alice', password='alice')
        self.parser = PlayerStatisticsParser(testdata, self.user1)
        self.player_stat_list = self.parser.parse()

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
        response = self.client.get('/ofm/players/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('player' in response.context_data)

    def test_user_cannot_see_other_users_players(self):
        self.client.login(username='bob', password='bob')
        response = self.client.get('/ofm/players/1')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('player' in response.context_data)
