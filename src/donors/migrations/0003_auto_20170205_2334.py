# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0002_auto_20170129_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_log',
            name='conversion_rate_if_not_PKR',
            field=models.IntegerField(default=1, verbose_name='Enter conversation rate, enter 1 for PKR'),
        ),
    ]
