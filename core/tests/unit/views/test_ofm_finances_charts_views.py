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

    def test_finance_balance_chart_json(self):
        response = self.client.get(reverse('core:ofm:finances_balance_chart_json'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)
        self.assertEqual('Kontostand', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])
        self.assertTrue('categories' in returned_json_data)

    def test_finance_income_chart_json(self):
        response = self.client.get(reverse('core:ofm:finances_income_chart_json'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)
        self.assertEqual('Ticketeinnahmen Liga', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])
        self.assertTrue('categories' in returned_json_data)

    def test_finance_expenses_chart_json(self):
        response = self.client.get(reverse('core:ofm:finances_expenses_chart_json'))
        self.assertEqual(response.status_code, 200)
        returned_json_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue('series' in returned_json_data)
        self.assertEqual('Spielergehalt', returned_json_data['series'][0]['name'])
        self.assertTrue('data' in returned_json_data['series'][0])
        self.assertTrue('categories' in returned_json_data)
