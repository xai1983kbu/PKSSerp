# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 22:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_school_shift'),
        ('classes', '0004_auto_20161230_2143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='class_section',
            new_name='school_class_section',
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together=set([('school', 'class_name', 'section')]),
        ),
    ]
