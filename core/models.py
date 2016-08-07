# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from users.models import OFMUser

AGE_AT_BIRTH = 17


class Season(models.Model):
    class Meta:
        ordering = ['-number']

    number = models.IntegerField()

    def __str__(self):
        return "%s" % self.number


class Quarter(models.Model):
    QUARTERS = ((0, '1'), (1, '2'), (2, '3'), (3, '4'))

    season = models.ForeignKey(Season)
    quarter = models.IntegerField(choices=QUARTERS)

    def __str__(self):
        return "%s/%s" % (self.season.number, self.quarter)


class Matchday(models.Model):
    class Meta:
        ordering = ['season', '-number']

    season = models.ForeignKey(Season)
    number = models.IntegerField()

    def __str__(self):
        return "%s/%s" % (self.season.number, self.number)


class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"

    COUNTRIES = (
        ('AF', "Afghanistan"),
        ('EG', "Ägypten"),
        ('AL', "Albanien"),
        ('DZ', "Algerien"),
        ('AD', "Andorra"),
        ('AO', "Angola"),
        ('AG', "Antigua und Barbuda"),
        ('GQ', "Äquatorialguinea"),
        ('AR', "Argentinien"),
        ('AM', "Armenien"),
        ('AZ', "Aserbaidschan"),
        ('ET', "Äthiopien"),
        ('AU', "Australien"),
        ('BS', "Bahamas"),
        ('BH', "Bahrain"),
        ('BD', "Bangladesch"),
        ('BB', "Barbados"),
        ('BE', "Belgien"),
        ('BZ', "Belize"),
        ('BJ', "Benin"),
        ('BT', "Bhutan"),
        ('BO', "Bolivien"),
        ('BA', "Bosnien und Herzegowina"),
        ('BW', "Botswana"),
        ('BR', "Brasilien"),
        ('BN', "Brunei"),
        ('BG', "Bulgarien"),
        ('BF', "Burkina Faso"),
        ('BI', "Burundi"),
        ('CL', "Chile"),
        ('TW', "Republik China (Taiwan)"),
        ('CN', "Volksrepublik China"),
        ('CR', "Costa Rica"),
        ('DK', "Dänemark"),
        ('DE', "Deutschland"),
        ('DM', "Dominica"),
        ('DO', "Dominikanische Republik"),
        ('DJ', "Dschibuti"),
        ('EC', "Ecuador"),
        ('CI', "Elfenbeinküste"),
        ('SV', "El Salvador"),
        ('ER', "Eritrea"),
        ('EE', "Estland"),
        ('FJ', "Fidschi"),
        ('FI', "Finnland"),
        ('FR', "Frankreich"),
        ('GA', "Gabun"),
        ('GM', "Gambia"),
        ('GE', "Georgien"),
        ('GH', "Ghana"),
        ('GD', "Grenada"),
        ('GR', "Griechenland"),
        ('GT', "Guatemala"),
        ('GN', "Guinea"),
        ('GW', "Guinea-Bissau"),
        ('GY', "Guyana"),
        ('HT', "Haiti"),
        ('HN', "Honduras"),
        ('IN', "Indien"),
        ('ID', "Indonesien"),
        ('IQ', "Irak"),
        ('IR', "Iran"),
        ('IE', "Irland"),
        ('IS', "Island"),
        ('IL', "Israel"),
        ('IT', "Italien"),
        ('JM', "Jamaika"),
        ('JP', "Japan"),
        ('YE', "Jemen"),
        ('JO', "Jordanien"),
        ('YUCS', "Jugoslawien"),
        ('KH', "Kambodscha"),
        ('CM', "Kamerun"),
        ('CA', "Kanada"),
        ('CV', "Kap Verde"),
        ('KZ', "Kasachstan"),
        ('QA', "Katar"),
        ('KE', "Kenia"),
        ('KG', "Kirgisistan"),
        ('KI', "Kiribati"),
        ('CO', "Kolumbien"),
        ('KM', "Komoren"),
        ('CG', "Republik Kongo"),
        ('CD', "Demokr. Republik Kongo"),
        ('KP', "Nordkorea"),
        ('KR', "Südkorea"),
        ('HR', "Kroatien"),
        ('CU', "Kuba"),
        ('KW', "Kuwait"),
        ('LA', "Laos"),
        ('LS', "Lesotho"),
        ('LV', "Lettland"),
        ('LB', "Libanon"),
        ('LR', "Liberia"),
        ('LY', "Libyen"),
        ('LI', "Liechtenstein"),
        ('LT', "Litauen"),
        ('LU', "Luxemburg"),
        ('MG', "Madagaskar"),
        ('MW', "Malawi"),
        ('MY', "Malaysia"),
        ('MV', "Malediven"),
        ('ML', "Mali"),
        ('MT', "Malta"),
        ('MA', "Marokko"),
        ('MH', "Marshallinseln"),
        ('MR', "Mauretanien"),
        ('MU', "Mauritius"),
        ('MK', "Mazedonien"),
        ('MX', "Mexiko"),
        ('FM', "Mikronesien"),
        ('MD', "Moldawien"),
        ('MC', "Monaco"),
        ('MN', "Mongolei"),
        ('ME', "Montenegro"),
        ('MZ', "Mosambik"),
        ('MM', "Myanmar"),
        ('NA', "Namibia"),
        ('NR', "Nauru"),
        ('NP', "Nepal"),
        ('NZ', "Neuseeland"),
        ('NI', "Nicaragua"),
        ('NL', "Niederlande"),
        ('NE', "Niger"),
        ('NG', "Nigeria"),
        ('NO', "Norwegen"),
        ('OM', "Oman"),
        ('AT', "Österreich"),
        ('TL', "Osttimor"),
        ('PK', "Pakistan"),
        ('PW', "Palau"),
        ('PA', "Panama"),
        ('PG', "Papua-Neuguinea"),
        ('PY', "Paraguay"),
        ('PE', "Peru"),
        ('PH', "Philippinen"),
        ('PL', "Polen"),
        ('PT', "Portugal"),
        ('RW', "Ruanda"),
        ('RO', "Rumänien"),
        ('RU', "Russland"),
        ('SB', "Salomonen"),
        ('ZM', "Sambia"),
        ('WS', "Samoa"),
        ('SM', "San Marino"),
        ('ST', "São Tomé und Príncipeão"),
        ('SA', "Saudi-Arabien"),
        ('SE', "Schweden"),
        ('CH', "Schweiz"),
        ('SN', "Senegal"),
        ('RS', "Serbien"),
        ('SC', "Seychellen"),
        ('SL', "Sierra Leone"),
        ('ZW', "Simbabwe"),
        ('SG', "Singapur"),
        ('SK', "Slowakei"),
        ('SI', "Slowenien"),
        ('SO', "Somalia"),
        ('ES', "Spanien"),
        ('LK', "Sri Lanka"),
        ('KN', "St Kitts und Nevis"),
        ('LC', "St Lucia"),
        ('VC', "St Vincent und die Grenadinen"),
        ('ZA', "Südafrika"),
        ('SD', "Sudan"),
        ('SS', "Südsudan"),
        ('SR', "Suriname"),
        ('SZ', "Swasiland"),
        ('SY', "Syrien"),
        ('TJ', "Tadschikistan"),
        ('TZ', "Tansania"),
        ('TH', "Thailand"),
        ('TG', "Togo"),
        ('TO', "Tonga"),
        ('TT', "Trinidad und Tobago"),
        ('TD', "Tschad"),
        ('CZ', "Tschechien"),
        ('TN', "Tunesien"),
        ('TR', "Türkei"),
        ('TM', "Turkmenistan"),
        ('TV', "Tuvalu"),
        ('UG', "Uganda"),
        ('UA', "Ukraine"),
        ('HU', "Ungarn"),
        ('UY', "Uruguay"),
        ('UZ', "Usbekistan"),
        ('VU', "Vanuatu"),
        ('VE', "Venezuela"),
        ('AE', "Vereinigte Arabische Emirate"),
        ('US', "Vereinigte Staaten von Amerika"),
        ('GB', "Vereinigtes Königreich"),
        ('VN', "Vietnam"),
        ('BY', "Weißrussland"),
        ('CF', "Zentralafrikanische Republik"),
        ('CY', "Zypern"),
        ('GB-ENG', "England"),
        ('GB-WLS', "Wales"),
        ('GB-SCT', "Schottland"),
        ('GB-NIR', "Nordirland"),
    )

    country = models.CharField(max_length=10, choices=COUNTRIES)

    def __str__(self):
        return dict(self.COUNTRIES).get(self.country)

    def get_iso(self):
        return self.country


class League(models.Model):
    LEAGUES = (
        (0, '1. Liga'),
        (1, '2. Liga'),
        (2, 'Regionalliga'),
        (3, 'Oberliga'),
        (4, 'Verbandsliga'),
        (5, 'Landesliga'),
        (6, 'Landesklasse'),
        (7, 'Bezirksliga'),
        (8, 'Bezirksklasse'),
        (9, 'Kreisliga'),
        (10, 'Kreisklasse'),
    )

    league = models.IntegerField(choices=LEAGUES)
    relay = models.CharField(max_length=10)
    country = models.ForeignKey(Country)

    def __str__(self):
        return "%s %s (%s)" % (self.LEAGUES[self.league][1], self.relay, self.country)


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

    name = models.CharField(max_length=200)
    position = models.CharField(max_length=3, choices=POSITIONS)
    nationality = models.ForeignKey(Country, blank=True, null=True)
    birth_season = models.ForeignKey(Season)

    def get_position(self):
        return dict(self.POSITIONS).get(self.position)

    def get_absolute_url(self):
        return reverse('core:ofm:player_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class PlayerStatistics(models.Model):
    class Meta:
        verbose_name_plural = "Player statistics"
        ordering = ['player', '-matchday']

    player = models.ForeignKey(Player, related_name='statistics')
    matchday = models.ForeignKey(Matchday, related_name='player_statistics')

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
        return self.matchday.season.number - self.player.birth_season.number

    def __str__(self):
        return "%s/%s: %s" % (self.matchday.season.number, self.matchday.number, self.player.name)


class Contract(models.Model):
    class Meta:
        ordering = ['user', 'player']

    player = models.ForeignKey(Player)
    user = models.ForeignKey(OFMUser)
    bought_on_matchday = models.ForeignKey(Matchday, related_name='bought_players')
    sold_on_matchday = models.ForeignKey(Matchday, blank=True, null=True, related_name='sold_players')

    def __str__(self):
        return "%s: %s" % (self.user.username, self.player.name)


class Finance(models.Model):
    class Meta:
        ordering = ['user', '-matchday']
        unique_together = (('user', 'matchday'),)

    user = models.ForeignKey(OFMUser)
    matchday = models.ForeignKey(Matchday)

    balance = models.IntegerField(default=0)

    income_visitors_league = models.IntegerField(default=0)
    income_sponsoring = models.IntegerField(default=0)
    income_cup = models.IntegerField(default=0)
    income_interests = models.IntegerField(default=0)
    income_loan = models.IntegerField(default=0)
    income_transfer = models.IntegerField(default=0)
    income_visitors_friendlies = models.IntegerField(default=0)
    income_friendlies = models.IntegerField(default=0)
    income_funcup = models.IntegerField(default=0)
    income_betting = models.IntegerField(default=0)

    expenses_player_salaries = models.IntegerField(default=0)
    expenses_stadium = models.IntegerField(default=0)
    expenses_youth = models.IntegerField(default=0)
    expenses_interests = models.IntegerField(default=0)
    expenses_trainings = models.IntegerField(default=0)
    expenses_transfer = models.IntegerField(default=0)
    expenses_compensation = models.IntegerField(default=0)
    expenses_friendlies = models.IntegerField(default=0)
    expenses_funcup = models.IntegerField(default=0)
    expenses_betting = models.IntegerField(default=0)

    def __str__(self):
        return "%s (%s): %s" % (self.user.username, self.matchday, self.balance)


class Match(models.Model):
    class Meta:
        ordering = ['user', '-matchday']
        verbose_name_plural = "Matches"

    MATCHTYPE = (
        ("L", "Liga"),
        ("F", "Friendly"),
        ("P", "Pokal"),
        ("F", "Fun-Cup"),
    )

    user = models.ForeignKey(OFMUser)
    matchday = models.ForeignKey(Matchday, related_name='matches')
    match_type = models.CharField(max_length=1, choices=MATCHTYPE, default='L')
    venue = models.CharField(max_length=200)  # should this be in MatchStadiumStatistics?
    home_team = models.CharField(max_length=200)
    guest_team = models.CharField(max_length=200)
    home_goals = models.IntegerField(default=0)
    guest_goals = models.IntegerField(default=0)

    def __str__(self):
        return "(%s) %s:%s - %s:%s" % (self.matchday, self.home_team, self.guest_team, self.home_goals, self.guest_goals)


# will only be created, if home match
class MatchStadiumStatistics(models.Model):
    class Meta:
        ordering = ['match']
        verbose_name_plural = "Match stadium statistics"

    match = models.OneToOneField(Match, related_name='stadium_statistics')

    @property
    def visitors(self):
        visitors = sum([stat.visitors for stat in self.stand_statistics])
        return visitors

    @property
    def capacity(self):
        capacity = sum([stat.capacity for stat in self.stand_statistics])
        return capacity

    def __str__(self):
        return "%s (%s): %s / %s" % (self.match.venue, self.match.matchday, self.visitors, self.capacity)


# always avoid alliterations.
class StadiumStandStatistics(models.Model):
    class Meta:
        verbose_name_plural = "Stadium stand statistics"

    SECTOR = (
        ("N", "Nord"),
        ("S", "Süd"),
        ("W", "West"),
        ("O", "Ost"),
    )

    stadium_statistics = models.ForeignKey(MatchStadiumStatistics, related_name="stand_statistics")
    sector = models.CharField(max_length=1, choices=SECTOR)
    capacity = models.IntegerField(default=0)
    visitors = models.IntegerField(default=0)
    ticket_price = models.IntegerField(default=0)
    condition = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return "%s / %s - %s - %s" % (self.visitors, self.capacity, self.ticket_price, self.condition)
