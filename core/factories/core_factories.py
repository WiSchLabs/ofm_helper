import factory

from core.models import Season, Quarter, Matchday, Player, PlayerStatistics, Contract, Country, Finance, Match, \
    MatchStadiumStatistics, StadiumStandStatistics, MatchTeamStatistics, StandLevel, StadiumLevel, StadiumLevelItem, \
    Checklist, ChecklistItem
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


class ChecklistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checklist

    user = factory.SubFactory(OFMUserFactory)


class ChecklistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChecklistItem

    checklist = factory.SubFactory(ChecklistFactory)
    name = "Item 1"
    last_checked = None
