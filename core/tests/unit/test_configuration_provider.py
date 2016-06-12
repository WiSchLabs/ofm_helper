import unittest

from django.conf import settings

from core.configuration_provider import ConfigurationProvider


class ConfigurationProviderTest(unittest.TestCase):
    def test_get_login_username(self):
        cp = ConfigurationProvider(settings.CONFIGURATION_FILE)
        username = cp.get('username')
        self.assertEqual(username, 'XXX')

    def test_get_login_password(self):
        cp = ConfigurationProvider(settings.CONFIGURATION_FILE)
        username = cp.get('password')
        self.assertEqual(username, '1234')
