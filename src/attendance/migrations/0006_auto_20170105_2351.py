# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 04:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_school_shift'),
        ('attendance', '0005_attendancecalendar_nonscheduledholidays'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nonscheduledholidays',
            old_name='date',
            new_name='holiday_date',
        ),
        migrations.AlterUniqueTogether(
            name='attendancecalendar',
            unique_together=set([('school', 'first_day_of_month')]),
        ),
        migrations.AlterUniqueTogether(
            name='nonscheduledholidays',
            unique_together=set([('school', 'holiday_date')]),
        ),
    ]
