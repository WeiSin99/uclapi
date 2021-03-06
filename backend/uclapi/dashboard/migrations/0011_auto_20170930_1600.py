# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-30 16:00
from __future__ import unicode_literals

import dashboard.app_helpers
from django.db import migrations, models
import django.db.models.deletion


def create_webhooks_for_existing_apps(apps, schema_editor):
    App = apps.get_model('dashboard', 'App')
    Webhook = apps.get_model('dashboard', 'Webhook')
    for app in App.objects.all():
        new_webhook = Webhook(app=app)
        new_webhook.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_unique_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, max_length=1000)),
                ('siteid', models.CharField(blank=True, max_length=40)),
                ('roomid', models.CharField(blank=True, max_length=160)),
                ('contact', models.CharField(blank=True, max_length=4000)),
                ('last_fired', models.DateTimeField(blank=True, null=True)),
                ('verification_secret', models.CharField(default=dashboard.app_helpers.generate_secret, max_length=100)),
                ('enabled', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookTriggerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payload', models.CharField(max_length=10000000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Webhook')),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='webhook',
            name='app',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.App'),
        ),
        migrations.RunPython(create_webhooks_for_existing_apps)
    ]
