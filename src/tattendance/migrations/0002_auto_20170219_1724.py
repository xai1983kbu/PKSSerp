# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_auto_20170218_1733'),
        ('tattendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherattendance',
            name='datestamp_change',
        ),
        migrations.AddField(
            model_name='teacherattendance',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schools.School'),
            preserve_default=False,
        ),
    ]