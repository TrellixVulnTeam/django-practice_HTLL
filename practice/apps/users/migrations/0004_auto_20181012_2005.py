# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-10-12 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181003_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(default=1, verbose_name='顺序'),
        ),
    ]