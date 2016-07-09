from core.models import Season, Quarter, Country, Matchday, League, Player, PlayerStatistics
from django.contrib import admin


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_filter = ['number']
    list_display = ['number', ]
    search_fields = ['number', ]


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_filter = ['quarter']
    list_display = ['season', 'quarter', ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_filter = ['country']
    list_display = ['country', ]
    search_fields = ['country', ]


@admin.register(Matchday)
class MatchdayAdmin(admin.ModelAdmin):
    list_display = ['season', 'number', ]
    search_fields = ['number', ]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['league', 'relay', 'country']
    search_fields = ['league', ]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ['position', 'nationality']
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(PlayerStatistics)
class SeasonAdmin(admin.ModelAdmin):
    list_filter = ['player', 'matchday']
    list_display = ['player', 'matchday']
    search_fields = ['player', ]
