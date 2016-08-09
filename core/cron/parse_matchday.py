from django_cron import CronJobBase, Schedule

from core.parsers.matchday_parser import MatchdayParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser


class ParseMatchdayCronJob(CronJobBase):
    RUN_AT_TIMES = ['03:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.cron.parse_matchday'

    def do(self):
        ofm_users = OFMUser.objects.exclude(ofm_username__isnull=True)

        site_manager = SiteManager(ofm_users[0] if ofm_users else None)
        site_manager.login()
        site_manager.jump_to_frame(Constants.HEAD)

        matchday_parser = MatchdayParser(site_manager.browser.page_source)
        current_matchday = matchday_parser.parse()

        site_manager.kill()

        print("parsed Matchday is: %s" % current_matchday)
