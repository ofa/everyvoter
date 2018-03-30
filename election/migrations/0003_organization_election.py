# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-29 16:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import kennedy_common.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('branding', '0001_initial'),
        ('election', '0002_load_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationElection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.Election')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branding.Organization', editable=False)),
            ],
            bases=(kennedy_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='organizationelection',
            unique_together=set([('organization', 'election')]),
        ),
    ]
