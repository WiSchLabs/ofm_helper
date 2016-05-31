import factory
from core.factories.core_factories import SeasonFactory, MatchdayFactory
from player_statistics.models import Player


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    position = 'TW'
    name = factory.Sequence(lambda n: 'Torwart%d' % n)
    nationality = "Deutschland"
    birth = factory.SubFactory(SeasonFactory)
    matchday = factory.SubFactory(MatchdayFactory)
