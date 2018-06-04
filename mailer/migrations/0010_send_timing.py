# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-28 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0009_remove_email_blocks_intermediate'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='send_finish',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Time Final Email Sent'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='send_start',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Time First Email Sent'),
        ),
    ]