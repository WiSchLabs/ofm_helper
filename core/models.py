from django.db import models

AGE_AT_BIRTH = 17


class Season(models.Model):
    class Meta:
        ordering = ['-number']

    number = models.IntegerField()


class Quarter(models.Model):
    QUARTERS = ((1, '1'), (2, '2'), (3, '3'), (4, '4'))

    season = models.ForeignKey(Season)
    quarter = models.IntegerField(choices=QUARTERS)


class Matchday(models.Model):
    class Meta:
        ordering = ['season', '-number']

    season = models.ForeignKey(Season)
    number = models.IntegerField()


# incomplete
class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"
    COUNTRIES = (
        (1, 'Ägypten'),
        (2, 'Bosnien und Herzegowina'),
        (3, 'Brasilien'),
        (4, 'Deutschland'),
        (5, 'England'),
        (6, 'Frankreich'),
        (7, 'Italien'),
        (8, 'Kuba'),
        (9, 'Neuseeland'),
        (10, 'Norwegen'),
        (11, 'Österreich'),
        (12, 'San Marino'),
        (13, 'Spanien'),
        (14, 'Türkei'),
        (15, 'Thailand'),
        (16, 'Ukraine'),
    )

    country = models.IntegerField(choices=COUNTRIES)


class League(models.Model):
    LEAGUES = (
        (1, '1. Liga'),
        (2, '2. Liga'),
        (3, 'Regionalliga'),
        (4, 'Oberliga'),
        (5, 'Verbandsliga'),
        (6, 'Landesliga'),
        (7, 'Landesklasse'),
        (8, 'Bezirksliga'),
        (9, 'Bezirksklasse'),
        (10, 'Kreisliga'),
        (11, 'Kreisklasse'),
    )

    league = models.IntegerField(choices=LEAGUES)
    relay = models.CharField(max_length=10)
    country = models.ForeignKey(Country)


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
    birthSeason = models.ForeignKey(Season)


class PlayerStatistics(models.Model):
    class Meta:
        verbose_name_plural = "Player statistics"
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

    @property
    def age(self):
        return (self.matchday.season.number - self.birthSeason.number) + AGE_AT_BIRTH
