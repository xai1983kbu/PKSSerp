# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 04:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_auto_20170105_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonscheduledholidays',
            name='holiday_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='nonscheduledholidays',
            name='reason_for_holiday',
            field=models.TextField(max_length=700),
        ),
    ]