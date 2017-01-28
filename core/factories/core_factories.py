import factory

from core.factories.matchday_related_core_factories import MatchdayFactory
from core.models import Checklist, ChecklistItem, Finance, ParsingSetting
from users.factories.users_factories import OFMUserFactory


class FinanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Finance

    user = factory.SubFactory(OFMUserFactory)
    matchday = factory.SubFactory(MatchdayFactory)

    balance = 1000

    income_visitors_league = 100
    income_sponsoring = 0
    income_cup = 0
    income_interests = 0
    income_loan = 0
    income_transfer = 0
    income_visitors_friendlies = 0
    income_friendlies = 0
    income_funcup = 0
    income_betting = 0

    expenses_player_salaries = 100
    expenses_stadium = 0
    expenses_youth = 0
    expenses_interests = 0
    expenses_trainings = 0
    expenses_transfer = 0
    expenses_compensation = 0
    expenses_friendlies = 0
    expenses_funcup = 0
    expenses_betting = 0


class ChecklistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checklist

    user = factory.SubFactory(OFMUserFactory)


class ChecklistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChecklistItem

    checklist = factory.SubFactory(ChecklistFactory)
    name = "Item 1"
    last_checked_on_matchday = None
    to_be_checked_on_matchdays = None
    to_be_checked_on_matchday_pattern = None
    to_be_checked_if_home_match_tomorrow = False
    is_inversed = False


class ParsingSettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParsingSetting

    user = factory.SubFactory(OFMUserFactory)
    parsing_chain_includes_player_statistics = True
    parsing_chain_includes_awp_boundaries = True
    parsing_chain_includes_finances = True
    parsing_chain_includes_matches = True
    parsing_chain_includes_match_details = False
    parsing_chain_includes_stadium_details = False
