import factory

from core.models import Season, Quarter, Matchday


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Season

    season = 1


class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    season = factory.SubFactory(SeasonFactory)
    quarter = 1


class MatchdayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Matchday

    season = factory.SubFactory(SeasonFactory)
    matchday = 1

