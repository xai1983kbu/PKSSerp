# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 19:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('student', 'attendance_date')]),
        ),
    ]
