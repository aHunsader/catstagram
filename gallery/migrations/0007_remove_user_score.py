# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 22:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_user_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='score',
        ),
    ]