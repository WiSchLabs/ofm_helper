import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import OFMUser


class OFMTransfersViewTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user(
            username='alice',
            email='alice@ofmhelper.com',
            password='alice',
            ofm_username='alice',
            ofm_password='alice'
        )
        self.client.login(username='alice', password='alice')

        self.json_response_keys = ["series", "categories", "ages", "strengths", "positions", "seasons", "matchdays"]
        self.all_strengths = list(range(1, 26))
        self.all_ages = list(range(17, 37))
        self.all_positions = ['LS', 'MS', 'RS', 'LM', 'ZM', 'RM', 'DM', 'VS', 'LIB', 'LV', 'LMD', 'RMD', 'RV', 'TW']

    def test_get_all_transfers_given_no_filters(self):
        response = self.client.get(reverse('core:ofm:transfers_detail_chart_json'))
        self.assertEqual(response.status_code, 200)

        returned_json_data = json.loads(response.content.decode('utf-8'))
        for key in self.json_response_keys:
            self.assertTrue(key in returned_json_data)

        for strength in self.all_strengths:
            self.assertTrue(strength in returned_json_data['strengths'])

        for age in self.all_ages:
            self.assertTrue(age in returned_json_data['ages'])

        for position in self.all_positions:
            self.assertTrue(position in returned_json_data['positions'])

    def test_get_transfers_with_all_positions(self):
        options = {'positions': 'All'}

        response = self.client.get(reverse('core:ofm:transfers_detail_chart_json'), options)
        self.assertEqual(response.status_code, 200)

        returned_json_data = json.loads(response.content.decode('utf-8'))
        for position in self.all_positions:
            self.assertTrue(position in returned_json_data['positions'])

    def test_get_transfers_with_empty_positions(self):
        options = {'positions': None}

        response = self.client.get(reverse('core:ofm:transfers_detail_chart_json'), options)
        self.assertEqual(response.status_code, 200)

        returned_json_data = json.loads(response.content.decode('utf-8'))
        for position in self.all_positions:
            self.assertTrue(position in returned_json_data['positions'])
