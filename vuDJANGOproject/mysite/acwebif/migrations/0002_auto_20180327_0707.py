# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-27 07:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acwebif', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mylog',
            old_name='pub_date',
            new_name='log_date',
        ),
    ]