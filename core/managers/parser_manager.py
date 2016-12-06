from bs4 import BeautifulSoup

from core.parsers.awp_boundaries_parser import AwpBoundariesParser
from core.parsers.finances_parser import FinancesParser
from core.parsers.future_match_row_parser import FutureMatchRowParser
from core.parsers.match_parser import MatchParser
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.ofm_helper_version_parser import OfmHelperVersionParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from core.parsers.stadium_statistics_parser import StadiumStatisticsParser
from core.parsers.won_by_default_match_row_parser import WonByDefaultMatchRowParser
from core.web.ofm_page_constants import Constants


class ParserManager:
    parsed_matchday = None
    players_already_parsed = False

    def parse_all_ofm_data(self, request, site_manager):
        self.parsed_matchday = self.parse_matchday(request, site_manager)
        self.parse_players(request, site_manager)
        self.players_already_parsed = True
        self.parse_player_statistics(request, site_manager)
        self.parse_awp_boundaries(request, site_manager)
        self.parse_finances(request, site_manager)
        self.parse_all_matches(request, site_manager)

        self.reset_parsing_flags()

    def reset_parsing_flags(self):
        self.parsed_matchday = None
        self.players_already_parsed = False

    def parse_ofm_version(self, site_manager):
        site_manager.jump_to_frame(Constants.GitHub.LATEST_RELEASE)
        version_parser = OfmHelperVersionParser(site_manager.browser.page_source)
        return version_parser.parse()

    def parse_matchday(self, request, site_manager):
        site_manager.jump_to_frame(Constants.HEAD)
        matchday_parser = MatchdayParser(site_manager.browser.page_source)
        return matchday_parser.parse()

    def parse_players(self, request, site_manager):
        if not self.parsed_matchday:
            self.parsed_matchday = self.parse_matchday(request, site_manager)
        site_manager.jump_to_frame(Constants.Team.PLAYERS)
        players_parser = PlayersParser(site_manager.browser.page_source, request.user, self.parsed_matchday)
        return players_parser.parse()

    def parse_player_statistics(self, request, site_manager):
        if not self.players_already_parsed:
            self.parse_players(request, site_manager)
        site_manager.jump_to_frame(Constants.Team.PLAYER_STATISTICS)
        player_stat_parser = PlayerStatisticsParser(site_manager.browser.page_source, request.user,
                                                    self.parsed_matchday)
        return player_stat_parser.parse()

    def parse_awp_boundaries(self, request, site_manager):
        if not self.parsed_matchday:
            self.parsed_matchday = self.parse_matchday(request, site_manager)
        site_manager.jump_to_frame(Constants.AWP_BOUNDARIES)
        awp_boundaries_parser = AwpBoundariesParser(site_manager.browser.page_source, request.user,
                                                    self.parsed_matchday)
        return awp_boundaries_parser.parse()

    def parse_finances(self, request, site_manager):
        if not self.parsed_matchday:
            self.parsed_matchday = self.parse_matchday(request, site_manager)
        site_manager.jump_to_frame(Constants.Finances.OVERVIEW)
        finances_parser = FinancesParser(site_manager.browser.page_source, request.user, self.parsed_matchday)
        return finances_parser.parse()

    def parse_all_matches(self, request, site_manager):
        if not self.parsed_matchday:
            self.parsed_matchday = self.parse_matchday(request, site_manager)
        site_manager.jump_to_frame(Constants.League.MATCH_SCHEDULE)
        soup = BeautifulSoup(site_manager.browser.page_source, "html.parser")

        rows = soup.find(id='table_head').find_all('tr')
        for row in rows:
            if row.has_attr("class"):  # exclude table header
                self._parse_single_match(request, site_manager, row)

    def _parse_single_match(self, request, site_manager, row):
        is_home_match = "black" in row.find_all('td')[1].a.get('class')
        match_report_image = row.find_all('img', class_='changeMatchReportImg')
        match_result = row.find('table').find_all('tr')[0].get_text().replace('\n', '').strip()
        is_current_matchday = int(row.find_all('td')[0].get_text()) == self.parsed_matchday.number

        if match_report_image:
            # match took place
            link_to_match = match_report_image[0].find_parent('a')['href']
            if "spielbericht" in link_to_match:
                site_manager.jump_to_frame(Constants.BASE + link_to_match)
                match_parser = MatchParser(site_manager.browser.page_source, request.user, is_home_match)
                match = match_parser.parse()

                if is_home_match and is_current_matchday:
                    self._parse_stadium_statistics(request, site_manager, match)

                return match
        elif "-:-" in match_result:
            # match is scheduled, but did not take place yet
            match_parser = FutureMatchRowParser(row, request.user)
            return match_parser.parse()
        else:
            match_parser = WonByDefaultMatchRowParser(row, request.user)
            return match_parser.parse()

    def _parse_stadium_statistics(self, request, site_manager, match):
        site_manager.jump_to_frame(Constants.Stadium.ENVIRONMENT)
        stadium_statistics_parser = StadiumStatisticsParser(site_manager.browser.page_source, request.user, match)
        stadium_statistics_parser.parse()

        site_manager.jump_to_frame(Constants.Stadium.OVERVIEW)
        stadium_stand_stat_parser = StadiumStandStatisticsParser(site_manager.browser.page_source, request.user, match)
        stadium_stand_stat_parser.parse()
