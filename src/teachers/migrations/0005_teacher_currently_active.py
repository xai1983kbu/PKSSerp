# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0004_auto_20170105_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='currently_active',
            field=models.BooleanField(default=True),
        ),
    ]
