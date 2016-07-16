from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from django_cron import CronJobBase, Schedule
from django_cron.models import CronJobLog
from users.models import OFMUser


class ParsePlayerStatisticsCronJob(CronJobBase):
    RUN_AT_TIMES = ['03:20']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'core.cron.parse_player_statistics'

    def do(self):
        players_parses = CronJobLog.objects.filter(code='core.cron.parse_players')
        if players_parses:
            last_players_cronjob_run = players_parses.order_by('-end_time')[0]

            print('1')
            print(last_players_cronjob_run.start_time)
            print(last_players_cronjob_run.end_time)
            print(last_players_cronjob_run.message)
            print(last_players_cronjob_run.is_success)

            if last_players_cronjob_run.is_success:
                print('2')
                for user in OFMUser.objects.all():
                    print('3')
                    print(user.username)
                    if user.ofm_username and user.ofm_password:
                        site_manager = SiteManager(user)
                        site_manager.login()
                        site_manager.jump_to_frame(Constants.TEAM.PLAYER_STATISTICS)

                        player_statistics_parser = PlayerStatisticsParser(site_manager.browser.page_source, user)
                        statistics = player_statistics_parser.parse()

                        site_manager.browser.quit()

                        print("parsed statistics count: %s" % len(statistics))
                        print("first parsed Statistic is: %s" % statistics[0])
            print('4')
