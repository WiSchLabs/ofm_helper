from django.test import TestCase

from core.parsers.parser_pipeline import ParserPipeline


class HomePageTest(TestCase):
    def test_parser_pipeline(self):
        pass
        # pipeline = ParserPipeline()
        # with mock.patch.object(pipeline.matchday_parser, 'url', open('core/tests/assets/head.html')):
        # ParserPipeline().parse_all()
