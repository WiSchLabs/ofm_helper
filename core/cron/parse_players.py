from core.cron.parse_matchday import ParseMatchdayCronJob
from core.parsers.players_parser import PlayersParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from django_cron import CronJobBase, Schedule
from users.models import OFMUser


class ParsePlayersCronJob(CronJobBase):
    #RUN_AT_TIMES = ['03:02']
    #schedule = Schedule(run_at_times=RUN_AT_TIMES)

    schedule = Schedule(run_every_mins=2)
    code = 'core.cron.parse_players'

    def do(self):

        matchday_success = ParseMatchdayCronJob.prev_success_cron()
        print("macthday success: %s" % matchday_success)

        if matchday_success:
            for user in OFMUser.objects.all():
                if user.ofm_username and user.ofm_password:
                    site_manager = SiteManager()
                    site_manager.login()
                    site_manager.jump_to_frame(Constants.TEAM.PLAYERS)

                    players_parser = PlayersParser(site_manager.browser.page_source, user)
                    players = players_parser.parse()

                    site_manager.browser.close()
                    site_manager.browser.quit()

                    print("parsed Player count: %s" % len(players))
                    print("first parsed Player is: %s" % players[0])
