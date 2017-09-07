# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 16:26
from __future__ import unicode_literals

from dashboard.app_helpers import generate_app_client_id, \
    generate_app_client_secret

from django.db import migrations


def populate_client_data(apps, schema_editor):
    App = apps.get_model('dashboard', 'App')
    for app in App.objects.all():
        app.client_id = generate_app_client_id()
        app.client_secret = generate_app_client_secret()
        app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20170701_1626'),
    ]

    operations = [
        migrations.RunPython(populate_client_data)
    ]
