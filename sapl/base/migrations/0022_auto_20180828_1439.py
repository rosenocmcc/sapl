# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-28 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20180821_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appconfig',
            name='esfera_federacao',
            field=models.CharField(blank=True, choices=[('M', 'Municipal'), ('E', 'Estadual'), ('F', 'Federal')], default='', max_length=1, verbose_name='Esfera Federação'),
        ),
    ]
