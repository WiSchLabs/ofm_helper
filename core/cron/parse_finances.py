from django_cron import CronJobBase, Schedule
from django_cron.models import CronJobLog

from core.parsers.finances_parser import FinancesParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser


class ParseFinancesCronJob(CronJobBase):
    RUN_AT_TIMES = ['03:30']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'core.cron.parse_finances'

    def do(self):
        matchday_parses = CronJobLog.objects.filter(code='core.cron.parse_matchday')
        #if matchday_parses:
        #    last_matchday_cronjob_run = matchday_parses.order_by('-end_time')[0]

            #if last_matchday_cronjob_run.is_success:
        for user in OFMUser.objects.all():
            if user.ofm_username and user.ofm_password:
                site_manager = SiteManager(user)
                site_manager.login()
                site_manager.jump_to_frame(Constants.FINANCES.OVERVIEW)

                print(site_manager.browser.page_source)

                finances_parser = FinancesParser(site_manager.browser.page_source, user)
                finances = finances_parser.parse()

                site_manager.browser.quit()

                print("parsed Finances is: %s" % finances)
