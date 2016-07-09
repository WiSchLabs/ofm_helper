from core.models import Matchday
from core.parsers.matchday_parser import MatchdayParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from django_cron import CronJobBase, Schedule


class ParseMatchdayCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.cron.parse_matchday'

    def do(self):
        site_manager = SiteManager()
        site_manager.login()
        site_manager.jump_to_frame(Constants.HEAD)

        matchday_parser = MatchdayParser(site_manager.browser.page_source)
        current_matchday = matchday_parser.parse()

        site_manager.browser.close()
        site_manager.browser.quit()

        print("parsed Matchday is: %s" % current_matchday)
