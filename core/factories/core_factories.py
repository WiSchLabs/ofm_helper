import factory

from core.models import Season, Quarter, Matchday, Player, PlayerStatistics


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


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    position = 'TW'
    name = factory.Sequence(lambda n: 'Torwart%d' % n)
    nationality = "Deutschland"
    birthSeason = factory.SubFactory(SeasonFactory)


class PlayerStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlayerStatistics

    player = factory.SubFactory(PlayerFactory)
    matchday = factory.SubFactory(MatchdayFactory)

    ep = 0
    tp = 0
    awp = 0
    strength = 1
    freshness = 0
    games_in_season = 0
    goals_in_season = 0
    won_tacklings_in_season = 0
    lost_tacklings_in_season = 0
    won_friendly_tacklings_in_season = 0
    lost_friendly_tacklings_in_season = 0
    yellow_cards_in_season = 0
    red_cards_in_season = 0
    equity = 0
