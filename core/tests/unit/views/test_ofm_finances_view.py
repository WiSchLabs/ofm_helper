import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory, FinanceFactory
from users.models import OFMUser


class OFMFinancesViewTestCase(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create()
        self.next_matchday = MatchdayFactory.create(number=1)
        self.user1 = OFMUser.objects.create_user(username='alice', email='alice@ofmhelper.com', password='alice',
                                                 ofm_username='alice', ofm_password='alice')
        self.finances = FinanceFactory.create(user=self.user1, matchday=self.matchday)
        self.next_finances = FinanceFactory.create(user=self.user1, matchday=self.next_matchday, balance=2000,
                                                   income_visitors_league=200, expenses_player_salaries=200)
        self.client.login(username='alice', password='alice')

    def test_user_can_see_his_finances(self):
        response = self.client.get(reverse('core:ofm:finance_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('matchdays' in response.context_data)

    def test_user_can_choose_between_matchdays(self):
        response = self.client.get(reverse('core:ofm:finance_overview'))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(self.next_matchday, response.context_data['matchdays'][0])
        self.assertEquals(self.matchday, response.context_data['matchdays'][1])

    def test_user_can_see_his_latest_finances_when_given_no_matchday(self):
        response = self.client.get(reverse('core:ofm:finances_json'))

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['account_balance'], 2000)
        self.assertEquals(returned_json_data[0]['income_visitors_league'], 200)
        self.assertEquals(returned_json_data[0]['expenses_player_salaries'], -200)

    def test_user_can_see_his_finances_diff_when_given_both_matchdays(self):
        third_matchday = MatchdayFactory.create(number=self.matchday.number + 2)
        FinanceFactory.create(user=self.user1, matchday=third_matchday, balance=2500, income_visitors_league=250,
                              income_sponsoring=250, expenses_player_salaries=250, expenses_youth=100)

        response = self.client.get(reverse('core:ofm:finances_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number,
                                    'older_matchday_season': self.matchday.season.number,
                                    'older_matchday': self.matchday.number
                                    })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['account_balance'], 2500)
        self.assertEquals(returned_json_data[0]['balance'], 150)
        self.assertEquals(returned_json_data[0]['sum_income'], 400)
        self.assertEquals(returned_json_data[0]['sum_expenses'], -250)
        self.assertEquals(returned_json_data[0]['income_visitors_league'], 150)
        self.assertEquals(returned_json_data[0]['expenses_player_salaries'], -150)

    def test_user_can_see_his_finances_diff_when_given_only_newer_matchday(self):
        third_matchday = MatchdayFactory.create(number=self.matchday.number + 2)
        FinanceFactory.create(user=self.user1, matchday=third_matchday, balance=2500, income_visitors_league=250,
                              expenses_player_salaries=250)

        response = self.client.get(reverse('core:ofm:finances_json'),
                                   {'newer_matchday_season': third_matchday.season.number,
                                    'newer_matchday': third_matchday.number
                                    })

        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(returned_json_data), 1)
        self.assertEquals(returned_json_data[0]['account_balance'], 2500)
        self.assertEquals(returned_json_data[0]['balance'], 0)
        self.assertEquals(returned_json_data[0]['sum_income'], 250)
        self.assertEquals(returned_json_data[0]['sum_expenses'], -250)
        self.assertEquals(returned_json_data[0]['income_visitors_league'], 250)
        self.assertEquals(returned_json_data[0]['expenses_player_salaries'], -250)
