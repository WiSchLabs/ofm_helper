# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-02 16:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_awpboundaries_awpboundarieskeyval'),
    ]

    operations = [
        migrations.RenameField(
            model_name='awpboundarieskeyval',
            old_name='value',
            new_name='awp',
        ),
        migrations.RenameField(
            model_name='awpboundarieskeyval',
            old_name='container',
            new_name='awp_boundaries',
        ),
        migrations.RenameField(
            model_name='awpboundarieskeyval',
            old_name='key',
            new_name='strength',
        ),
    ]
