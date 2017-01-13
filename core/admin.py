from core.models import Season, Quarter, Country, Matchday, League, Player, PlayerStatistics, Contract, Finance, \
    Match, MatchStadiumStatistics, StadiumStandStatistics, StandLevel, StadiumLevel, MatchTeamStatistics, \
    StadiumLevelItem, AwpBoundaries, Checklist, ChecklistItem, ParsingSetting
from django.contrib import admin


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['number']
    search_fields = ['number']


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_filter = ['quarter']
    list_display = ['season', 'quarter']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country']
    search_fields = ['country']


@admin.register(Matchday)
class MatchdayAdmin(admin.ModelAdmin):
    list_display = ['season', 'number']


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['league', 'relay', 'country']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ['position', 'nationality']
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(PlayerStatistics)
class PlayerStatisticsAdmin(admin.ModelAdmin):
    list_filter = ['matchday']
    list_display = ['player', 'matchday']
    search_fields = ['player', 'matchday']


@admin.register(AwpBoundaries)
class AwpBoundariesAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    fields = ['name']
    search_fields = ['name']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_filter = ['player', 'user']
    search_fields = ['player', 'user__username']


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_filter = ['user', 'matchday']
    list_display = ['user', 'matchday']
    search_fields = ['user__username', 'matchday__number']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = ['user', 'matchday']
    list_display = ['user', 'matchday']
    search_fields = ['user__username', 'matchday__number']


@admin.register(MatchStadiumStatistics)
class MatchStadiumStatisticsAdmin(admin.ModelAdmin):
    list_filter = ['match__user', 'match__matchday']
    list_display = ['match']
    search_fields = ['match__user__username', 'match__matchday__number']


@admin.register(StadiumStandStatistics)
class StadiumStandStatisticsAdmin(admin.ModelAdmin):
    list_filter = ['stadium_statistics__match__user', 'stadium_statistics__match__matchday']
    list_display = ['stadium_statistics']
    search_fields = ['stadium_statistics__match__user__username', 'stadium_statistics__match__matchday__number']


@admin.register(MatchTeamStatistics)
class MatchTeamStatisticsAdmin(admin.ModelAdmin):
    list_filter = ['team_name']
    list_display = ['team_name']
    search_fields = ['team_name']


@admin.register(StandLevel)
class StandLevelAdmin(admin.ModelAdmin):
    list_display = ['capacity', 'has_roof', 'has_seats']
    search_fields = ['capacity', 'has_roof', 'has_seats']


@admin.register(StadiumLevel)
class StadiumLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(StadiumLevelItem)
class StadiumLevelItemAdmin(admin.ModelAdmin):
    list_display = ['current_level', 'value', 'daily_costs']
    search_fields = ['current_level', 'value', 'daily_costs']


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user__username']


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_filter = ['checklist__user', 'name']
    list_display = ['priority',
                    'name',
                    'to_be_checked_on_matchdays',
                    'to_be_checked_on_matchday_pattern',
                    'to_be_checked_if_home_match_tomorrow']
    search_fields = ['checklist__user__username', 'name']


@admin.register(ParsingSetting)
class ParsingSettingAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user',
                    'parsing_chain_includes_player_statistics',
                    'parsing_chain_includes_awp_boundaries',
                    'parsing_chain_includes_finances',
                    'parsing_chain_includes_matches',
                    'parsing_chain_includes_match_details',
                    'parsing_chain_includes_stadium_details']
    search_fields = ['user__username']
