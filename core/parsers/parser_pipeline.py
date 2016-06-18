from core.parsers.matchday_parser import MatchdayParser


class ParserPipeline:
    def __init__(self):
        self.matchday_parser = MatchdayParser()

    def parse_all(self):
        pass