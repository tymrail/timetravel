# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authonline', '0010_route_route_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='route_modified_time',
            field=models.DateField(auto_now=True),
        ),
    ]