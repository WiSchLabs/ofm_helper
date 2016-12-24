import factory

from core.models import Season, Quarter, Matchday, Player, PlayerStatistics, Contract, Country, Finance, Match, \
    MatchStadiumStatistics, StadiumStandStatistics, MatchTeamStatistics, StandLevel, StadiumLevel, StadiumLevelItem, \
    Checklist, ChecklistItem, ParsingSetting
from users.factories.users_factories import OFMUserFactory


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Season

    number = 1


class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    season = factory.SubFactory(SeasonFactory)
    quarter = 1


class MatchdayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Matchday

    season = factory.SubFactory(SeasonFactory)
    number = 0
