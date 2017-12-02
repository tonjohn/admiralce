# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-13 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='fee',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
