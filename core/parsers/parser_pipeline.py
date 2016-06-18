from core.parsers.matchday_parser import MatchdayParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser


class ParserPipeline:
    def __init__(self, parsers=[MatchdayParser(), PlayerStatisticsParser()]):
        self.parsers = parsers

    def parse_all(self):
        for parser in self.parsers:
            parser.parse()
