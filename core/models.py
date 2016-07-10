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
        (0, 'Afghanistan'),
        (1, 'Ägypten'),
        (2, 'Albanien'),
        (3, 'Algerien'),
        (4, 'Andorra'),
        (5, 'Angola'),
        (6, 'Antigua und Barbuda'),
        (7, 'Äquatorialguinea'),
        (8, 'Argentinien'),
        (9, 'Armenien'),
        (10, 'Aserbaidschan'),
        (11, 'Äthiopien'),
        (12, 'Australien'),
        (13, 'Bahamas'),
        (14, 'Bahrain'),
        (15, 'Bangladesch'),
        (16, 'Barbados'),
        (17, 'Belgien'),
        (18, 'Belize'),
        (19, 'Benin'),
        (20, 'Bhutan'),
        (21, 'Bolivien'),
        (22, 'Bosnien und Herzegowina'),
        (23, 'Botswana'),
        (24, 'Brasilien'),
        (25, 'Brunei'),
        (26, 'Bulgarien'),
        (27, 'Burkina Faso'),
        (28, 'Burundi'),
        (29, 'Chile'),
        (30, 'Republik China (Taiwan)'),
        (31, 'Volksrepublik China'),
        (32, 'Costa Rica'),
        (33, 'Dänemark'),
        (34, 'Deutschland'),
        (35, 'Dominica'),
        (36, 'Dominikanische Republik'),
        (37, 'Dschibuti'),
        (38, 'Ecuador'),
        (39, 'Elfenbeinküste'),
        (40, 'El Salvador'),
        (41, 'Eritrea'),
        (42, 'Estland'),
        (43, 'Fidschi'),
        (44, 'Finnland'),
        (45, 'Frankreich'),
        (46, 'Gabun'),
        (47, 'Gambia'),
        (48, 'Georgien'),
        (49, 'Ghana'),
        (50, 'Grenada'),
        (51, 'Griechenland'),
        (52, 'Guatemala'),
        (53, 'Guinea'),
        (54, 'Guinea-Bissau'),
        (55, 'Guyana'),
        (56, 'Haiti'),
        (57, 'Honduras'),
        (58, 'Indien-Indien'),
        (59, 'Indonesien'),
        (60, 'Irak'),
        (61, 'Iran'),
        (62, 'Irland'),
        (63, 'Island'),
        (64, 'Israel'),
        (65, 'Italien'),
        (66, 'Jamaika'),
        (67, 'Japan'),
        (68, 'Jemen'),
        (69, 'Jordanien'),
        (70, 'Jugoslawien'),
        (71, 'Kambodscha'),
        (72, 'Kamerun'),
        (73, 'Kanada'),
        (74, 'Kap Verde'),
        (75, 'Kasachstan'),
        (76, 'Katar'),
        (77, 'Kenia'),
        (78, 'Kirgisistan'),
        (79, 'Kiribati'),
        (80, 'Kolumbien'),
        (81, 'Komoren'),
        (82, 'Republik Kongo'),
        (83, 'Demokratische Republik Kongo'),
        (84, 'Nordkorea'),
        (85, 'Südkorea'),
        (86, 'Kroatien'),
        (87, 'Kuba'),
        (88, 'Kuwait'),
        (89, 'Laos'),
        (90, 'Lesotho'),
        (91, 'Lettland'),
        (92, 'Libanon'),
        (93, 'Liberia'),
        (94, 'Libyen'),
        (95, 'Liechtenstein'),
        (96, 'Litauen'),
        (97, 'Luxemburg'),
        (98, 'Madagaskar'),
        (99, 'Malawi'),
        (100, 'Malaysia'),
        (101, 'Malediven'),
        (102, 'Mali'),
        (103, 'Malta'),
        (104, 'Marokko'),
        (105, 'Marshallinseln'),
        (106, 'Mauretanien'),
        (107, 'Mauritius'),
        (108, 'Mazedonien'),
        (109, 'Mexiko'),
        (110, 'Mikronesien'),
        (111, 'Moldawien'),
        (112, 'Monaco'),
        (113, 'Mongolei'),
        (114, 'Montenegro'),
        (115, 'Mosambik'),
        (116, 'Myanmar'),
        (117, 'Namibia'),
        (118, 'Nauru'),
        (119, 'Nepal'),
        (120, 'Neuseeland'),
        (121, 'Nicaragua'),
        (122, 'Niederlande'),
        (123, 'Niger'),
        (124, 'Nigeria'),
        (125, 'Norwegen'),
        (126, 'Oman'),
        (127, 'Österreich'),
        (128, 'Osttimor'),
        (129, 'Pakistan'),
        (130, 'Palau'),
        (131, 'Panama'),
        (132, 'Papua-Neuguinea'),
        (133, 'Paraguay'),
        (134, 'Peru'),
        (135, 'Philippinen'),
        (136, 'Polen'),
        (137, 'Portugal'),
        (138, 'Ruanda'),
        (139, 'Rumänien'),
        (140, 'Russland'),
        (141, 'Salomonen'),
        (142, 'Sambia'),
        (143, 'Samoa'),
        (144, 'San Marino'),
        (145, 'São Tomé und Príncipeão'),
        (146, 'Saudi-Arabien'),
        (147, 'Schweden'),
        (148, 'Schweiz'),
        (149, 'Senegal'),
        (150, 'Serbien'),
        (151, 'Seychellen'),
        (152, 'Sierra Leone'),
        (153, 'Simbabwe'),
        (154, 'Singapur'),
        (155, 'Slowakei'),
        (156, 'Slowenien'),
        (157, 'Somalia'),
        (158, 'Spanien'),
        (159, 'Sri Lanka'),
        (160, 'St Kitts und Nevis'),
        (161, 'St Lucia'),
        (162, 'St Vincent und die Grenadinen'),
        (163, 'Südafrika'),
        (164, 'Sudan'),
        (165, 'Südsudan'),
        (166, 'Suriname'),
        (167, 'Swasiland'),
        (168, 'Syrien'),
        (169, 'Tadschikistan'),
        (170, 'Tansania'),
        (171, 'Thailand'),
        (172, 'Togo'),
        (173, 'Tonga'),
        (174, 'Trinidad und Tobago'),
        (175, 'Tschad'),
        (176, 'Tschechien'),
        (177, 'Tunesien'),
        (178, 'Türkei'),
        (179, 'Turkmenistan'),
        (180, 'Tuvalu'),
        (181, 'Uganda'),
        (182, 'Ukraine'),
        (183, 'Ungarn'),
        (184, 'Uruguay'),
        (185, 'Usbekistan'),
        (186, 'Vanuatu'),
        (187, 'Venezuela'),
        (188, 'Vereinigte Arabische Emirate'),
        (189, 'Vereinigte Staaten von Amerika'),
        (190, 'Vereinigtes Königreich'),
        (191, 'Vietnam'),
        (192, 'Weißrussland'),
        (193, 'Zentralafrikanische Republik'),
        (194, 'Zypern'),
        (195, 'England'),
        (196, 'Wales'),
        (197, 'Schottland'),
        (198, 'Nordirland'),
    )

    country = models.IntegerField(choices=COUNTRIES)

    def __str__(self):
        print(self.COUNTRIES[self.country])
        return self.COUNTRIES[self.country]
        #if self.country:
        #    return self.COUNTRIES[self.country][1]
        #else:
        #    return ""


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

    class Meta:
        ordering = ['position']

    name = models.CharField(max_length=200)
    position = models.CharField(max_length=3, choices=POSITIONS)
    nationality = models.ForeignKey(Country, blank=True, null=True)
    birth_season = models.ForeignKey(Season)

    def get_absolute_url(self):
        return reverse('core:ofm:player_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


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
        return self.matchday.season.number - self.player.birth_season.number

    def __str__(self):
        return "%s/%s: %s" % (self.matchday.season.number, self.matchday.number, self.player.name)


class PlayerUserOwnership(models.Model):
    player = models.ForeignKey(Player)
    user = models.ForeignKey(OFMUser)
    bought_on_matchday = models.ForeignKey(Matchday, related_name='bought_players')
    sold_on_matchday = models.ForeignKey(Matchday, blank=True, null=True, related_name='sold_players')

    def __str__(self):
        return "%s: %s " % (self.user.username, self.player.name)
