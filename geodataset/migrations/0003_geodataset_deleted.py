# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-30 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodataset', '0002_foreign_relationships'),
    ]

    operations = [
        migrations.AddField(
            model_name='geodataset',
            name='deleted',
            field=models.BooleanField(db_index=True, default=False, editable=False, verbose_name=b'Deleted'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='fields',
            field=models.ManyToManyField(blank=True, through='geodataset.FieldValue', to='geodataset.Field'),
        ),
    ]