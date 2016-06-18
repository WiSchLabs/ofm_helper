import factory

from core.models import Season, Quarter, Matchday, Player


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
    number = 1


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    position = 'TW'
    name = factory.Sequence(lambda n: 'Torwart%d' % n)
    nationality = "Deutschland"
    birthSeason = factory.SubFactory(SeasonFactory)
    matchday = factory.SubFactory(MatchdayFactory)

