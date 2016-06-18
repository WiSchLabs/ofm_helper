from django.test import TestCase

from core.parsers.parser_pipeline import ParserPipeline


class HomePageTest(TestCase):
    def test_parser_pipeline(self):
        ParserPipeline.parse_all()
