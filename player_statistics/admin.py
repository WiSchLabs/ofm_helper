from django.contrib import admin

from player_statistics.models import PlayerStatistics, Player

admin.site.register(Player)
admin.site.register(PlayerStatistics)
