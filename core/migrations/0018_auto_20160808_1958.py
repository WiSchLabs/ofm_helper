# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160807_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchTeamStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('score', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('ball_possession', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('chances', models.IntegerField(default=0)),
                ('yellow_cards', models.IntegerField(default=0)),
                ('red_cards', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'MatchTeamStatistics',
            },
        ),
        migrations.CreateModel(
            name='StadiumLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StadiumLevelItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_level', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=0)),
                ('daily_costs', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-current_level', '-value', '-daily_costs'],
            },
        ),
        migrations.CreateModel(
            name='StandLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(default=0)),
                ('has_roof', models.BooleanField(default=False)),
                ('has_seats', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='guest_goals',
        ),
        migrations.RemoveField(
            model_name='match',
            name='guest_team',
        ),
        migrations.RemoveField(
            model_name='match',
            name='home_goals',
        ),
        migrations.RemoveField(
            model_name='match',
            name='home_team',
        ),
        migrations.RemoveField(
            model_name='stadiumstandstatistics',
            name='capacity',
        ),
        migrations.AddField(
            model_name='stadiumlevel',
            name='light',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stadium_levels_light', to='core.StadiumLevelItem'),
        ),
        migrations.AddField(
            model_name='stadiumlevel',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stadium_levels_parking', to='core.StadiumLevelItem'),
        ),
        migrations.AddField(
            model_name='stadiumlevel',
            name='screen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stadium_levels_screen', to='core.StadiumLevelItem'),
        ),
        migrations.AddField(
            model_name='stadiumlevel',
            name='security',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stadium_levels_security', to='core.StadiumLevelItem'),
        ),
        migrations.AddField(
            model_name='match',
            name='guest_team_statistics',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_guest_team', to='core.MatchTeamStatistics'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='home_team_statistics',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_home_team', to='core.MatchTeamStatistics'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matchstadiumstatistics',
            name='level',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='stadium_statistics', to='core.StadiumLevel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stadiumstandstatistics',
            name='level',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='stand_statistics', to='core.StandLevel'),
            preserve_default=False,
        ),
    ]
