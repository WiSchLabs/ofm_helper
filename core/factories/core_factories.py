import factory

from core.models import Season, Quarter


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Season

    season = 1


class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    season = factory.SubFactory(SeasonFactory)
    quarter = 1
