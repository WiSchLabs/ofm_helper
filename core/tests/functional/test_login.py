import time
import unittest

from django.conf import settings
from selenium import webdriver

from core.configuration_provider import ConfigurationProvider

TESTDATA_PATH = 'core/config'


class CreateCoreModelsTest(unittest.TestCase):
    def setUp(self):
        if settings.USE_DISPLAY_FOR_AWS:
            from pyvirtualdisplay import Display
            self.display = Display(visible=0, size=(1024, 768))
            self.display.start()
        self.browser = webdriver.Firefox()
        self.browser.get("http://v7.www.onlinefussballmanager.de/")
        cfg = ConfigurationProvider()
        self.login_user = cfg.get("credentials", "OFM_USERNAME")
        self.login_password = cfg.get("credentials", "OFM_PASSWORD")

    def tearDown(self):
        self.browser.quit()
        if settings.USE_DISPLAY_FOR_AWS:
            self.display.stop()

    def test_login(self):
        self.assertNotIn("OFM", self.browser.title)
        self.login()
        self.assertIn("OFM", self.browser.title)

    def login(self):
        link_login_account = self.browser.find_element_by_xpath("//div[@id='register_div']//a")
        link_login_account.click()
        time.sleep(1)
        login_field_user = self.browser.find_element_by_xpath("//form[@id='login_form']//input[@id='login']")
        login_field_user.send_keys(self.login_user)
        login_field_password = self.browser.find_element_by_xpath("//form[@id='login_form']//input[@id='password']")
        login_field_password.send_keys(self.login_password)
        login_button = self.browser.find_element_by_xpath("//form[@id='login_form']//button[@id='logingrafikbutton']")
        login_button.click()
        time.sleep(1)
