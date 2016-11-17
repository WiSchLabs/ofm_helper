# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-16 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country',
            field=models.CharField(choices=[('AF', 'Afghanistan'), ('EG', 'Ägypten'), ('AL', 'Albanien'), ('DZ', 'Algerien'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AG', 'Antigua und Barbuda'), ('GQ', 'Äquatorialguinea'), ('AR', 'Argentinien'), ('AM', 'Armenien'), ('AZ', 'Aserbaidschan'), ('ET', 'Äthiopien'), ('AU', 'Australien'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesch'), ('BB', 'Barbados'), ('BE', 'Belgien'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BT', 'Bhutan'), ('BO', 'Bolivien'), ('BA', 'Bosnien und Herzegowina'), ('BW', 'Botswana'), ('BR', 'Brasilien'), ('BN', 'Brunei'), ('BG', 'Bulgarien'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('CL', 'Chile'), ('TW', 'Republik China (Taiwan)'), ('CN', 'Volksrepublik China'), ('CR', 'Costa Rica'), ('DK', 'Dänemark'), ('DE', 'Deutschland'), ('DM', 'Dominica'), ('DO', 'Dominikanische Republik'), ('DJ', 'Dschibuti'), ('EC', 'Ecuador'), ('CI', 'Elfenbeinküste'), ('SV', 'El Salvador'), ('ER', 'Eritrea'), ('EE', 'Estland'), ('FJ', 'Fidschi'), ('FI', 'Finnland'), ('FR', 'Frankreich'), ('GA', 'Gabun'), ('GM', 'Gambia'), ('GE', 'Georgien'), ('GH', 'Ghana'), ('GD', 'Grenada'), ('GR', 'Griechenland'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('IN', 'Indien'), ('ID', 'Indonesien'), ('IQ', 'Irak'), ('IR', 'Iran'), ('IE', 'Irland'), ('IS', 'Island'), ('IL', 'Israel'), ('IT', 'Italien'), ('JM', 'Jamaika'), ('JP', 'Japan'), ('YE', 'Jemen'), ('JO', 'Jordanien'), ('YUCS', 'Jugoslawien'), ('KH', 'Kambodscha'), ('CM', 'Kamerun'), ('CA', 'Kanada'), ('CV', 'Kap Verde'), ('KZ', 'Kasachstan'), ('QA', 'Katar'), ('KE', 'Kenia'), ('KG', 'Kirgisistan'), ('KI', 'Kiribati'), ('CO', 'Kolumbien'), ('KM', 'Komoren'), ('CG', 'Republik Kongo'), ('CD', 'Demokr. Republik Kongo'), ('KP', 'Nordkorea'), ('KR', 'Südkorea'), ('HR', 'Kroatien'), ('CU', 'Kuba'), ('KW', 'Kuwait'), ('LA', 'Laos'), ('LS', 'Lesotho'), ('LV', 'Lettland'), ('LB', 'Libanon'), ('LR', 'Liberia'), ('LY', 'Libyen'), ('LI', 'Liechtenstein'), ('LT', 'Litauen'), ('LU', 'Luxemburg'), ('MG', 'Madagaskar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Malediven'), ('ML', 'Mali'), ('MT', 'Malta'), ('MA', 'Marokko'), ('MH', 'Marshallinseln'), ('MR', 'Mauretanien'), ('MU', 'Mauritius'), ('MK', 'Mazedonien'), ('MX', 'Mexiko'), ('FM', 'Mikronesien'), ('MD', 'Moldawien'), ('MC', 'Monaco'), ('MN', 'Mongolei'), ('ME', 'Montenegro'), ('MZ', 'Mosambik'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NZ', 'Neuseeland'), ('NI', 'Nicaragua'), ('NL', 'Niederlande'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NO', 'Norwegen'), ('OM', 'Oman'), ('AT', 'Österreich'), ('TL', 'Osttimor'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua-Neuguinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippinen'), ('PL', 'Polen'), ('PT', 'Portugal'), ('RW', 'Ruanda'), ('RO', 'Rumänien'), ('RU', 'Russland'), ('SB', 'Salomonen'), ('ZM', 'Sambia'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'São Tomé und Príncipeão'), ('SA', 'Saudi-Arabien'), ('SE', 'Schweden'), ('CH', 'Schweiz'), ('SN', 'Senegal'), ('RS', 'Serbien'), ('SC', 'Seychellen'), ('SL', 'Sierra Leone'), ('ZW', 'Simbabwe'), ('SG', 'Singapur'), ('SK', 'Slowakei'), ('SI', 'Slowenien'), ('SO', 'Somalia'), ('ES', 'Spanien'), ('LK', 'Sri Lanka'), ('KN', 'St Kitts und Nevis'), ('LC', 'St Lucia'), ('VC', 'St Vincent und die Grenadinen'), ('ZA', 'Südafrika'), ('SD', 'Sudan'), ('SS', 'Südsudan'), ('SR', 'Suriname'), ('SZ', 'Swasiland'), ('SY', 'Syrien'), ('TJ', 'Tadschikistan'), ('TZ', 'Tansania'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TO', 'Tonga'), ('TT', 'Trinidad und Tobago'), ('TD', 'Tschad'), ('CZ', 'Tschechien'), ('TN', 'Tunesien'), ('TR', 'Türkei'), ('TM', 'Turkmenistan'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('HU', 'Ungarn'), ('UY', 'Uruguay'), ('UZ', 'Usbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('AE', 'Vereinigte Arabische Emirate'), ('US', 'USA'), ('GB', 'Vereinigtes Königreich'), ('VN', 'Vietnam'), ('BY', 'Weißrussland'), ('CF', 'Zentralafrikanische Republik'), ('CY', 'Zypern'), ('GB-ENG', 'England'), ('GB-WLS', 'Wales'), ('GB-SCT', 'Schottland'), ('GB-NIR', 'Nordirland')], max_length=10),
        ),
    ]
