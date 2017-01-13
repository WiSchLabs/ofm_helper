import factory

from core.factories.matchday_related_core_factories import MatchdayFactory
from core.models import Match, MatchStadiumStatistics, MatchTeamStatistics, StadiumStandStatistics, \
                        StadiumLevel, StadiumLevelItem, StandLevel
from users.factories.users_factories import OFMUserFactory


class MatchTeamStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MatchTeamStatistics

    team_name = 'Springfield Isotopes'
    score = 0
    strength = 50
    ball_possession = 50
    chances = 3
    yellow_cards = 2
    red_cards = 0


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Match

    user = factory.SubFactory(OFMUserFactory)
    matchday = factory.SubFactory(MatchdayFactory)
    is_home_match = True
    match_type = 'L'
    venue = 'Olympiastadion Berlin'
    home_team_statistics = factory.SubFactory(MatchTeamStatisticsFactory)
    guest_team_statistics = factory.SubFactory(MatchTeamStatisticsFactory)


class StadiumLevelItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StadiumLevelItem

    current_level = 0
    value = 0
    daily_costs = 0


class StadiumLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StadiumLevel

    light = factory.SubFactory(StadiumLevelItemFactory)
    screen = factory.SubFactory(StadiumLevelItemFactory)
    security = factory.SubFactory(StadiumLevelItemFactory)
    parking = factory.SubFactory(StadiumLevelItemFactory)


class MatchStadiumStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MatchStadiumStatistics

    match = factory.SubFactory(MatchFactory)
    level = factory.SubFactory(StadiumLevelFactory)


class StandLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StandLevel

    capacity = 100
    has_roof = False
    has_seats = False


class StadiumStandStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StadiumStandStatistics

    stadium_statistics = factory.SubFactory(MatchStadiumStatisticsFactory)
    level = factory.SubFactory(StandLevelFactory)
    sector = 'N'
    visitors = 42
    ticket_price = 55
    condition = 99.42
