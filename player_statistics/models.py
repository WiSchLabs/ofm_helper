from django.db import models


class Player(models.Model):
    position = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=17)
    strength = models.IntegerField(default=1)
    freshness = models.IntegerField(default=1)
    games = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)


class SeasonedPlayerStatistics(models.Model):
    player = models.ForeignKey(Player)
    season = models.IntegerField(default=1)
    games = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    won_tacklings = models.IntegerField(default=0)
    lost_tacklings = models.IntegerField(default=0)
    won_friendly_tacklings = models.IntegerField(default=0)
    lost_friendly_tacklings = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)


class DailyPlayerStatistics(models.Model):
    player = models.ForeignKey(Player)
    ep = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    awp = models.IntegerField(default=0)
