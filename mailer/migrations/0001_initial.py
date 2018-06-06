# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-30 16:37
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_smalluuid.models
import everyvoter_common.utils.models
import rendering.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(db_index=True, default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('subject', models.CharField(max_length=100, validators=[rendering.validators.validate_template], verbose_name=b'Subject Line')),
                ('pre_header', models.CharField(blank=True, max_length=100, null=True, validators=[rendering.validators.validate_template], verbose_name=b'Pre-Header Text')),
                ('from_name', models.CharField(max_length=50, verbose_name=b'From Name')),
                ('body_above', models.TextField(blank=True, validators=[rendering.validators.validate_template], verbose_name=b'Email Body Above')),
                ('body_below', models.TextField(blank=True, validators=[rendering.validators.validate_template], verbose_name=b'Email Body Below')),
            ],
            options={
                'abstract': False,
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='EmailActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('message_id', models.CharField(max_length=100, verbose_name=b'Message ID from ESP')),
                ('activity', models.CharField(choices=[(b'send', b'Sent'), (b'bounce', b'Bounce'), (b'soft_bounce', b'Soft Bounce'), (b'complaint', b'Complaint'), (b'open', b'Open'), (b'click', b'Click')], max_length=50, verbose_name=b'Action Type')),
                ('link', models.CharField(default=None, max_length=500, null=True, verbose_name=b'Click URL')),
            ],
            options={
                'verbose_name': 'Email Activity',
                'verbose_name_plural': 'Email Activities',
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='EmailCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('organization', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='branding.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='EmailWrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(db_index=True, default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('header', models.TextField(validators=[rendering.validators.validate_template], verbose_name=b'Header')),
                ('footer', models.TextField(validators=[rendering.validators.validate_template], verbose_name=b'Footer')),
                ('default', models.BooleanField(default=False, verbose_name=b'Default')),
                ('organization', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='branding.Organization')),
            ],
            options={
                'verbose_name': 'Email Wrapper',
                'verbose_name_plural': 'Email Wrappers',
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('from_email', models.EmailField(max_length=254, verbose_name=b'From Email')),
                ('stats', django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name=b'Stats')),
                ('source', models.CharField(max_length=100, verbose_name=b'Source Code')),
                ('count', models.IntegerField(default=0, verbose_name=b'Recipients')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailer.Email')),
            ],
            options={
                'verbose_name': 'Mailing',
                'verbose_name_plural': 'Mailings',
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='MailingTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('deadline_type', models.CharField(choices=[(b'vr_deadline', b'Registration'), (b'evip_start_date', b'Early Vote Start'), (b'evip_close_date', b'Early Vote End'), (b'vbm_application_deadline', b'Vote By Mail Applications Due'), (b'vbm_return_date', b'Vote By Mail Returns Due'), (b'election_date', b'Election Day')], max_length=50, verbose_name=b'Deadline Type')),
                ('election_type', models.CharField(choices=[(b'primary', b'Federal Primary'), (b'general', b'Federal General'), (b'special', b'Federal Special')], max_length=50, verbose_name=b'Election Type')),
                ('days_to_deadline', models.IntegerField(default=0, verbose_name=b'Days to Deadline')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailer.Email')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'ordering': ['election_type', 'deadline_type', '-days_to_deadline']
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='SendingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('address', models.EmailField(max_length=254, verbose_name=b'Email Address')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eligible_addresses', to='branding.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.CreateModel(
            name='Unsubscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(db_index=True, default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('origin', models.CharField(choices=[(b'user', b'Manual'), (b'bounce', b'Bounce'), (b'complaint', b'Complaint')], max_length=50)),
                ('reason', models.CharField(blank=True, max_length=255, verbose_name=b'Reason')),
                ('global_unsub', models.BooleanField(db_index=True, default=False, verbose_name=b'Applies Globally')),
                ('mailing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailer.Mailing')),
                ('organization', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='branding.Organization')),
            ],
            options={
                'verbose_name': 'Unsubscribe',
                'verbose_name_plural': 'Unsubscribes',
            },
            bases=(everyvoter_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.AddField(
            model_name='mailing',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailer.MailingTemplate'),
        ),
        migrations.AddField(
            model_name='emailactivity',
            name='mailing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailer.Mailing'),
        ),
        migrations.AddField(
            model_name='email',
            name='categories',
            field=models.ManyToManyField(blank=True, to='mailer.EmailCategory'),
        ),
        migrations.AddField(
            model_name='email',
            name='organization',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='branding.Organization'),
        ),
    ]
