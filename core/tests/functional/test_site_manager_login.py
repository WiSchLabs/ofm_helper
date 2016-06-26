import unittest

from core.configuration_provider import ConfigurationProvider
from django.conf import settings

from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.site_manager = SiteManager()
        self.site_manager.login()

    def tearDown(self):
        self.site_manager.browser.quit()
        if settings.USE_DISPLAY_FOR_AWS:
            self.site_manager.display.stop()

    def test_login_with_config_provider(self):
        self.assertIn("OFM", self.site_manager.browser.title)

    def test_head_page(self):
        self.site_manager.browser.get(Constants.HEAD)
        self.assertIn("Spieltag", self.site_manager.browser.page_source)
        self.assertIn("Saison", self.site_manager.browser.page_source)
        self.assertIn("Team", self.site_manager.browser.page_source)
        self.assertIn("Liga", self.site_manager.browser.page_source)

    def test_login_with_user(self):
        config = ConfigurationProvider()
        ofm_username = config.get('credentials', 'OFM_USERNAME')
        ofm_password = config.get('credentials', 'OFM_PASSWORD')
        user = OFMUser('name', 'mail@pro.com', 'pass', ofm_username=ofm_username, ofm_password=ofm_password)
        self.site_manager = SiteManager(user)
        self.site_manager.login()
        self.assertIn("OFM", self.site_manager.browser.title)
