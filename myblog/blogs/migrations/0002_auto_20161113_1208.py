# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.CharField(max_length=10, verbose_name='旅游景点'),
        ),
    ]
