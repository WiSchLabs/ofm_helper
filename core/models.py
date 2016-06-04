from django.db import models


class Season(models.Model):
    number = models.IntegerField()


class Quarter(models.Model):
    QUARTERS = ((1, '1'), (2, '2'), (3, '3'), (4, '4'))

    season = models.ForeignKey(Season)
    quarter = models.IntegerField(choices=QUARTERS)


class Matchday(models.Model):
    season = models.ForeignKey(Season)
    matchday = models.IntegerField()


# incomplete
class Country(models.Model):
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


# not quite correct? 2. Liga Nord, 2. Liga Süd etc.
# how to generate them properly?
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
