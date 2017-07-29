# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='created_at',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AddField(
            model_name='registration',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]