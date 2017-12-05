# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-12-04 18:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materia', '0019_auto_20171127_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orgao',
            options={'ordering': ['nome'], 'verbose_name': 'Órgão', 'verbose_name_plural': 'Órgãos'},
        ),
        migrations.AlterModelOptions(
            name='tipodocumento',
            options={'ordering': ['descricao'], 'verbose_name': 'Tipo de Documento', 'verbose_name_plural': 'Tipos de Documento'},
        ),
        migrations.AlterModelOptions(
            name='unidadetramitacao',
            options={'verbose_name': 'Unidade de Tramitação', 'verbose_name_plural': 'Unidades de Tramitação'},
        ),
    ]