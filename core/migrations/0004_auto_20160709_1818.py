# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160709_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='birthSeason',
            new_name='birth_season',
        ),
        migrations.AlterField(
            model_name='country',
            name='country',
            field=models.IntegerField(choices=[(0, 'Afghanistan'), (1, 'Ägypten'), (2, 'Albanien'), (3, 'Algerien'), (4, 'Andorra'), (5, 'Angola'), (6, 'Antigua und Barbuda'), (7, 'Äquatorialguinea'), (8, 'Argentinien'), (9, 'Armenien'), (10, 'Aserbaidschan'), (11, 'Äthiopien'), (12, 'Australien'), (13, 'Bahamas'), (14, 'Bahrain'), (15, 'Bangladesch'), (16, 'Barbados'), (17, 'Belgien'), (18, 'Belize'), (19, 'Benin'), (20, 'Bhutan'), (21, 'Bolivien'), (22, 'Bosnien und Herzegowina'), (23, 'Botswana'), (24, 'Brasilien'), (25, 'Brunei'), (26, 'Bulgarien'), (27, 'Burkina Faso'), (28, 'Burundi'), (29, 'Chile'), (30, 'Republik China (Taiwan)'), (31, 'Volksrepublik China'), (32, 'Costa Rica'), (33, 'Dänemark'), (34, 'Deutschland'), (35, 'Dominica'), (36, 'Dominikanische Republik'), (37, 'Dschibuti'), (38, 'Ecuador'), (39, 'Elfenbeinküste'), (40, 'El Salvador'), (41, 'Eritrea'), (42, 'Estland'), (43, 'Fidschi'), (44, 'Finnland'), (45, 'Frankreich'), (46, 'Gabun'), (47, 'Gambia'), (48, 'Georgien'), (49, 'Ghana'), (50, 'Grenada'), (51, 'Griechenland'), (52, 'Guatemala'), (53, 'Guinea'), (54, 'Guinea-Bissau'), (55, 'Guyana'), (56, 'Haiti'), (57, 'Honduras'), (58, 'Indien-Indien'), (59, 'Indonesien'), (60, 'Irak'), (61, 'Iran'), (62, 'Irland'), (63, 'Island'), (64, 'Israel'), (65, 'Italien'), (66, 'Jamaika'), (67, 'Japan'), (68, 'Jemen'), (69, 'Jordanien'), (70, 'Jugoslawien'), (71, 'Kambodscha'), (72, 'Kamerun'), (73, 'Kanada'), (74, 'Kap Verde'), (75, 'Kasachstan'), (76, 'Katar'), (77, 'Kenia'), (78, 'Kirgisistan'), (79, 'Kiribati'), (80, 'Kolumbien'), (81, 'Komoren'), (82, 'Republik Kongo'), (83, 'Demokratische Republik Kongo'), (84, 'Nordkorea'), (85, 'Südkorea'), (86, 'Kroatien'), (87, 'Kuba'), (88, 'Kuwait'), (89, 'Laos'), (90, 'Lesotho'), (91, 'Lettland'), (92, 'Libanon'), (93, 'Liberia'), (94, 'Libyen'), (95, 'Liechtenstein'), (96, 'Litauen'), (97, 'Luxemburg'), (98, 'Madagaskar'), (99, 'Malawi'), (100, 'Malaysia'), (101, 'Malediven'), (102, 'Mali'), (103, 'Malta'), (104, 'Marokko'), (105, 'Marshallinseln'), (106, 'Mauretanien'), (107, 'Mauritius'), (108, 'Mazedonien'), (109, 'Mexiko'), (110, 'Mikronesien'), (111, 'Moldawien'), (112, 'Monaco'), (113, 'Mongolei'), (114, 'Montenegro'), (115, 'Mosambik'), (116, 'Myanmar'), (117, 'Namibia'), (118, 'Nauru'), (119, 'Nepal'), (120, 'Neuseeland'), (121, 'Nicaragua'), (122, 'Niederlande'), (123, 'Niger'), (124, 'Nigeria'), (125, 'Norwegen'), (126, 'Oman'), (127, 'Österreich'), (128, 'Osttimor'), (129, 'Pakistan'), (130, 'Palau'), (131, 'Panama'), (132, 'Papua-Neuguinea'), (133, 'Paraguay'), (134, 'Peru'), (135, 'Philippinen'), (136, 'Polen'), (137, 'Portugal'), (138, 'Ruanda'), (139, 'Rumänien'), (140, 'Russland'), (141, 'Salomonen'), (142, 'Sambia'), (143, 'Samoa'), (144, 'San Marino'), (145, 'São Tomé und Príncipeão'), (146, 'Saudi-Arabien'), (147, 'Schweden'), (148, 'Schweiz'), (1590, 'Senegal'), (151, 'Serbien'), (152, 'Seychellen'), (153, 'Sierra Leone'), (154, 'Simbabwe'), (155, 'Singapur'), (156, 'Slowakei'), (157, 'Slowenien'), (158, 'Somalia'), (159, 'Spanien'), (15, 'Sri Lanka'), (160, 'St Kitts und Nevis'), (161, 'St Lucia'), (162, 'St Vincent und die Grenadinen'), (163, 'Südafrika'), (164, 'Sudan'), (165, 'Südsudan'), (166, 'Suriname'), (167, 'Swasiland'), (168, 'Syrien'), (169, 'Tadschikistan'), (170, 'Tansania'), (171, 'Thailand'), (172, 'Togo'), (173, 'Tonga'), (174, 'Trinidad und Tobago'), (175, 'Tschad'), (176, 'Tschechien'), (177, 'Tunesien'), (178, 'Türkei'), (179, 'Turkmenistan'), (180, 'Tuvalu'), (181, 'Uganda'), (182, 'Ukraine'), (183, 'Ungarn'), (184, 'Uruguay'), (185, 'Usbekistan'), (186, 'Vanuatu'), (187, 'Venezuela'), (188, 'Vereinigte Arabische Emirate'), (189, 'Vereinigte Staaten von Amerika'), (190, 'Vereinigtes Königreich'), (191, 'Vietnam'), (192, 'Weißrussland'), (193, 'Zentralafrikanische Republik'), (194, 'Zypern'), (195, 'England'), (196, 'Wales'), (197, 'Schottland'), (198, 'Nordirland')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='nationality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Country'),
        ),
    ]
