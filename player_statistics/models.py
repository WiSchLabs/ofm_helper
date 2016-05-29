from core.models import Season, Matchday, CurrentMatchday
from django.db import models


AGE_AT_BIRTH = 17


class Player(models.Model):
    POSITIONS = (
        ("TW", "Torwart"),
        ("LIB", "Libero"),
        ("LV", "Linker Verteidiger"),
        ("LMD", "Linker Manndecker"),
        ("RMD", "Rechter Manndecker"),
        ("RV", "Rechter Verteidiger"),
        ("VS", "Vorstopper"),
        ("LM", "Linkes Mittelfeld"),
        ("DM", "Defensives Mittelfeld"),
        ("ZM", "Zentrales Mittelfeld"),
        ("RM", "Rechtes Mittelfeld"),
        ("LS", "Linker Stürmer"),
        ("MS", "Mittelstürmer"),
        ("RS", "Rechter Stürmer")
    )

    class Meta:
        ordering = ['position']

    position = models.CharField(max_length=3, choices=POSITIONS)
    name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    birth = models.ForeignKey(Season)
    current_matchday = models.ForeignKey(CurrentMatchday)

    @property
    def age(self):
        return (self.current_matchday.matchday.season.season - self.birth.season) + AGE_AT_BIRTH


class PlayerStatistics(models.Model):
    class Meta:
        order_with_respect_to = 'player'

    player = models.ForeignKey(Player)
    matchday = models.ForeignKey(Matchday)

    ep = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    awp = models.IntegerField(default=0)
    strength = models.IntegerField(default=1)
    freshness = models.IntegerField(default=0)
    games_in_season = models.IntegerField(default=0)
    goals_in_season = models.IntegerField(default=0)
    won_tacklings_in_season = models.IntegerField(default=0)
    lost_tacklings_in_season = models.IntegerField(default=0)
    won_friendly_tacklings_in_season = models.IntegerField(default=0)
    lost_friendly_tacklings_in_season = models.IntegerField(default=0)
    yellow_cards_in_season = models.IntegerField(default=0)
    red_cards_in_season = models.IntegerField(default=0)
    equity = models.IntegerField(default=0)
