# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum_conversation", "0004_auto_20160427_0502"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="approved",
            field=models.BooleanField(
                db_index=True, default=True, verbose_name="Approved"
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="approved",
            field=models.BooleanField(
                db_index=True, default=True, verbose_name="Approved"
            ),
        ),
    ]
