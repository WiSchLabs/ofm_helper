from bs4 import BeautifulSoup
from django_cron import CronJobBase, Schedule
from django_cron.models import CronJobLog

from core.parsers.match_parser import MatchParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser


class ParseMatchesCronJob(CronJobBase):
    RUN_AT_TIMES = ['03:40']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'core.cron.parse_matches'

    def do(self):
        matchday_parses = CronJobLog.objects.filter(code='core.cron.parse_matchday')
        if matchday_parses:
            last_matchday_cronjob_run = matchday_parses.order_by('-end_time')[0]

            if last_matchday_cronjob_run.is_success:
                for user in OFMUser.objects.all():
                    if user.ofm_username and user.ofm_password and user.is_active:
                        site_manager = SiteManager(user)
                        site_manager.login()
                        site_manager.jump_to_frame(Constants.LEAGUE.MATCHDAY_TABLE)

                        soup = BeautifulSoup(site_manager.browser.page_source, "html.parser")
                        row = soup.find(id='table_head').find_all('b')[0].find_parent('tr')
                        link_to_match = row.find_all('img')[0].find_parent('a')['href']
                        if "spielbericht" in link_to_match:
                            # only parse match if statistics are available
                            # as match don't take place if one team did not have a valid team setup
                            site_manager.jump_to_frame(Constants.BASE + link_to_match)
                            match_parser = MatchParser(site_manager.browser.page_source, user)
                            match = match_parser.parse()

                        site_manager.kill()

                        print("parsed Match is: %s" % match)
