from core.models import Season, Quarter, Country, Matchday, League, Player, PlayerStatistics, Contract
from django.contrib import admin
from django.contrib.admin import register


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['number', ]
    search_fields = ['number', ]


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_filter = ['quarter']
    list_display = ['season', 'quarter', ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country', ]
    search_fields = ['country', ]


@admin.register(Matchday)
class MatchdayAdmin(admin.ModelAdmin):
    list_display = ['season', 'number', ]


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


@admin.register(Contract)
class PlayerUserOwnershipAdmin(admin.ModelAdmin):
    list_filter = ['player', 'user']
    search_fields = ['player', 'user']


