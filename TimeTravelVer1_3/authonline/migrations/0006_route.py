# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 13:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authonline', '0005_city_city_img_src'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('route_id', models.AutoField(primary_key=True, serialize=False)),
                ('route_name', models.CharField(default='', max_length=64)),
                ('route_detail', models.CharField(max_length=512)),
                ('route_owner', models.ManyToManyField(related_name='route', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
