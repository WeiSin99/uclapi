# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roombookings', '0009_sitelocation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PageToken',
        ),
    ]