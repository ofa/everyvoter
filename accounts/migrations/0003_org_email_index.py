# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_foreign_relationships'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=[b'organization', b'email'], name=b'org_email_idx'),
        ),
    ]