# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0002_auto_20150725_0512"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="forum",
            name="is_active",
        ),
    ]
