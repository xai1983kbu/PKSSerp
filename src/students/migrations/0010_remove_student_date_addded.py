# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 22:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_student_date_addded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='date_addded',
        ),
    ]
