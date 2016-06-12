import os
import unittest

from core.configuration_provider import ConfigurationProvider

TESTDATA_PATH = 'core/tests/assets/'


class ConfigurationProviderTest(unittest.TestCase):
    def test_get_login_username(self):
        cp = ConfigurationProvider(os.path.join(TESTDATA_PATH, 'config.txt'))
        username = cp.get('username')
        self.assertEqual(username, 'XXX')

    def test_get_login_password(self):
        cp = ConfigurationProvider(os.path.join(TESTDATA_PATH, 'config.txt'))
        username = cp.get('password')
        self.assertEqual(username, '1234')
