import configparser
import os
import time
import unittest

from pyvirtualdisplay import Display
from selenium import webdriver

TESTDATA_PATH = 'core/config'


class CreateCoreModelsTest(unittest.TestCase):
    def setUp(self):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        self.browser = webdriver.Firefox()
        self.browser.get("http://v7.www.onlinefussballmanager.de/")
        config = configparser.ConfigParser()
        config.read(os.path.join(TESTDATA_PATH, 'test.cfg'))
        self.login_user = config.get("configuration", "username")
        self.login_password = config.get("configuration", "password")

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        if self.login_user == "XXX":
            return unittest.skip("login credentials not set")
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
