# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-19 05:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_bpost_user_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpost',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bpost',
            name='publish_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
