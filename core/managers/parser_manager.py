from bs4 import BeautifulSoup

from core.models import Matchday
from core.parsers.awp_boundaries_parser import AwpBoundariesParser
from core.parsers.finances_parser import FinancesParser
from core.parsers.match_parser import MatchParser
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.ofm_helper_version_parser import OfmHelperVersionParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from core.parsers.stadium_statistics_parser import StadiumStatisticsParser
from core.parsers.won_by_default_match_parser import WonByDefaultMatchParser
from core.web.ofm_page_constants import Constants


class ParserManager:
    def parse_all_ofm_data(self, request, site_manager):
        self.parse_matchday(request, site_manager)
        self.parse_players(request, site_manager)
        self.parse_player_statistics(request, site_manager)
        self.parse_awp_boundaries(request, site_manager)
        self.parse_finances(request, site_manager)
    
        matchday = Matchday.objects.all()[0]
    
        if matchday.number > 0:
            #  do not parse on matchday 0
            self.parse_match(request, site_manager)

    def parse_ofm_version(self, site_manager):
        site_manager.jump_to_frame(Constants.GITHUB.LATEST_RELEASE)
        version_parser = OfmHelperVersionParser(site_manager.browser.page_source)
        return version_parser.parse()
    
    def parse_matchday(self, request, site_manager):
        site_manager.jump_to_frame(Constants.HEAD)
        matchday_parser = MatchdayParser(site_manager.browser.page_source)
        return matchday_parser.parse()
    
    def parse_players(self, request, site_manager):
        site_manager.jump_to_frame(Constants.TEAM.PLAYERS)
        players_parser = PlayersParser(site_manager.browser.page_source, request.user)
        return players_parser.parse()

    def parse_player_statistics(self, request, site_manager):
        site_manager.jump_to_frame(Constants.TEAM.PLAYER_STATISTICS)
        player_stat_parser = PlayerStatisticsParser(site_manager.browser.page_source, request.user)
        return player_stat_parser.parse()
    
    
    def parse_awp_boundaries(self, request, site_manager):
        site_manager.jump_to_frame(Constants.AWP_BOUNDARIES)
        awp_boundaries_parser = AwpBoundariesParser(site_manager.browser.page_source, request.user)
        return awp_boundaries_parser.parse()

    def parse_finances(self, request, site_manager):
        site_manager.jump_to_frame(Constants.FINANCES.OVERVIEW)
        finances_parser = FinancesParser(site_manager.browser.page_source, request.user)
        return finances_parser.parse()
    
    def parse_match(self, request, site_manager):
        if Matchday.objects.all()[0].number <= 0:
            return
    
        site_manager.jump_to_frame(Constants.LEAGUE.MATCHDAY_TABLE)
        soup = BeautifulSoup(site_manager.browser.page_source, "html.parser")
        row = soup.find(id='table_head').find_all('b')[0].find_parent('tr')
        is_home_match = "<b>" in str(row.find_all('td')[2].a)
        match_report_image = row.find_all('img', class_='changeMatchReportImg')
    
        if match_report_image:
            # match took place
            link_to_match = match_report_image[0].find_parent('a')['href']
            if "spielbericht" in link_to_match:
                site_manager.jump_to_frame(Constants.BASE + link_to_match)
                match_parser = MatchParser(site_manager.browser.page_source, request.user, is_home_match)
                match = match_parser.parse()
    
                if is_home_match:
                    self.parse_stadium_statistics(request, site_manager)
    
                return match
        else:
            match_parser = WonByDefaultMatchParser(site_manager.browser.page_source, request.user)
            return match_parser.parse()
    
    def parse_stadium_statistics(self, request, site_manager):
        site_manager.jump_to_frame(Constants.STADIUM.ENVIRONMENT)
        stadium_statistics_parser = StadiumStatisticsParser(site_manager.browser.page_source, request.user)
        stadium_statistics_parser.parse()
        site_manager.jump_to_frame(Constants.STADIUM.OVERVIEW)
        stadium_stand_stat_parser = StadiumStandStatisticsParser(site_manager.browser.page_source, request.user)
        return stadium_stand_stat_parser.parse()
