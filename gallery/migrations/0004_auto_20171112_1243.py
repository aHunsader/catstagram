# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20171112_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='uploads/Profiles/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(upload_to='uploads/Posts/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
