# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_auto_20171112_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.TextField(blank=True),
        ),
    ]
