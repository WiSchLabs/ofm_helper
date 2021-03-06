import factory

from core.factories.matchday_related_core_factories import MatchdayFactory, SeasonFactory
from core.models import Contract, Country, Player, PlayerStatistics
from users.factories.users_factories import OFMUserFactory


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    country = 'DE'


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    position = 'TW'
    name = factory.Sequence(lambda n: 'Martin Adomeit')
    nationality = factory.SubFactory(CountryFactory)
    birth_season = factory.SubFactory(SeasonFactory)


class PlayerStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlayerStatistics

    player = factory.SubFactory(PlayerFactory)
    matchday = factory.SubFactory(MatchdayFactory)

    ep = 2
    tp = 5
    awp = 3
    strength = 1
    freshness = 4
    games_in_season = 0
    goals_in_season = 0
    won_tacklings_in_season = 0
    lost_tacklings_in_season = 0
    won_friendly_tacklings_in_season = 0
    lost_friendly_tacklings_in_season = 0
    yellow_cards_in_season = 0
    red_cards_in_season = 0
    equity = 0


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    player = factory.SubFactory(PlayerFactory)
    user = factory.SubFactory(OFMUserFactory)
    bought_on_matchday = factory.SubFactory(MatchdayFactory)
    sold_on_matchday = None
