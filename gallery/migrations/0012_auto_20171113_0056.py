# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 08:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0011_auto_20171112_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
    ]