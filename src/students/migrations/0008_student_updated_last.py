# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_student_updated_last_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='updated_last',
            field=models.DateField(auto_now=True),
        ),
    ]
