import os
from core.configuration_provider import ConfigurationProvider
from django.test import TestCase


class ConfigurationProviderTest(TestCase):
    def setUp(self):
        self.cp = ConfigurationProvider()

    def test_get_login_username_from_config(self):
        username = self.cp.get('credentials', 'OFM_USERNAME', use_env_vars=False)
        self.assertEqual(username, 'XXX')

    def test_get_login_password_from_config(self):
        password = self.cp.get('credentials', 'OFM_PASSWORD', use_env_vars=False)
        self.assertEqual(password, '1234')

    def test_override_env_variable_and_get_correct_result(self):
        if os.environ.get('OFM_USERNAME'):
            curr = os.environ['OFM_USERNAME']
        else:
            curr = ''
        os.environ['OFM_USERNAME'] = 'YYY'
        username = self.cp.get('credentials', 'OFM_USERNAME')
        self.assertEqual(username, 'YYY')
        os.environ['OFM_USERNAME'] = curr
