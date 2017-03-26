import os
import time

from django.conf import settings
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from timeout_decorator import timeout
from timeout_decorator.timeout_decorator import TimeoutError  # pylint: disable=redefined-builtin
from xvfbwrapper import Xvfb

from core.models import Matchday
from core.web.ofm_page_constants import Constants
from ofm_helper.common_settings import BASE_DIR


class OFMSiteManager:
    def __init__(self, user=None):
        self.user = user

        if settings.PHANTOMJS_REMOTE:
            self.browser = webdriver.Remote(command_executor='http://{}:8910'.format(settings.PHANTOMJS_HOST),
                                            desired_capabilities=DesiredCapabilities.PHANTOMJS)
        else:
            self.browser = webdriver.PhantomJS()

        self._handle_aws_display_bug()

        if self.user:
            self._login_user = self.user.ofm_username
            self._login_password = self.user.ofm_password
        else:
            self._login_user = os.environ('OFM_USERNAME')
            self._login_password = os.environ('OFM_PASSWORD')

    def login(self):
        self.browser.get(Constants.BASE)
        self._switch_to_login_div()

        self._insert_login_credentials()
        self._click_login_button()

    def jump_to_frame(self, frame):
        self.browser.get(frame)

    def kill_browser(self):
        self.browser.stop_client()
        self.browser.close()
        self.browser.quit()

    def _handle_aws_display_bug(self):
        if settings.USE_DISPLAY_FOR_AWS:
            from pyvirtualdisplay import Display
            self.display = Display(visible=0, size=(1024, 768))
            self.display.start()

    def _switch_to_login_div(self):
        link_login_account = self.browser.find_element_by_xpath("//div[@id='register_div']//a")
        link_login_account.click()
        time.sleep(1)

    def _insert_login_credentials(self):
        login_field_user = self.browser.find_element_by_xpath("//form[@id='login_form']//input[@id='login']")
        login_field_user.send_keys(self._login_user)
        login_field_password = self.browser.find_element_by_xpath("//form[@id='login_form']//input[@id='password']")
        login_field_password.send_keys(self._login_password)

    def _click_login_button(self):
        login_button = self.browser.find_element_by_xpath("//form[@id='login_form']//button[@id='logingrafikbutton']")
        login_button.click()
        time.sleep(1)


class OFMTransferSiteManager(OFMSiteManager):
    def __init__(self, user=None):  # pylint: disable=super-init-not-called
        self.user = user
        if self.user:
            self._login_user = self.user.ofm_username
            self._login_password = self.user.ofm_password
        else:
            self._login_user = os.environ('OFM_USERNAME')
            self._login_password = os.environ('OFM_PASSWORD')

        self.display = Xvfb()
        self.display.start()

    def download_transfer_excel(self, matchday=None):
        if not self._is_transfer_file_present(matchday):
            profile = webdriver.FirefoxProfile(os.path.join(BASE_DIR, 'ofm_transfer_data', 'firefox_profile'))
            profile.set_preference("browser.download.dir", os.path.join(BASE_DIR, 'ofm_transfer_data'))
            self.browser = webdriver.Firefox(firefox_profile=profile)

            self.login()

            try:
                self._jump_to_transfer_page(self, matchday=matchday)  # pylint: disable=redundant-keyword-arg
            except TimeoutError:
                pass

    @staticmethod
    def _is_transfer_file_present(matchday=None):

        if not matchday:
            matchday = Matchday.get_current()

        if os.path.isfile(os.path.join(BASE_DIR,
                                           'ofm_transfer_data',
                                           'ofm_spielerwechsel_{}_{}.csv'.format(
                                                matchday.season.number,
                                                matchday.number)
                                           )):
            return True
        return False

    @timeout(5, use_signals=False)
    def _jump_to_transfer_page(self, matchday=None):
        if not matchday:
            self.jump_to_frame(Constants.Transfer.DOWNLOAD_TRANSFERS)
        else:
            self.jump_to_frame(Constants.Transfer.DOWNLOAD_TRANSFERS_FROM_MATCHDAY.format(matchday.number))

    def kill_browser(self):
        self.browser.stop_client()
        self.display.stop()
