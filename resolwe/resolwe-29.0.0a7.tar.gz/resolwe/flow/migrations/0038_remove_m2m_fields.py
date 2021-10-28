# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0037_migrate_m2o"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collection",
            name="data",
        ),
        migrations.RemoveField(
            model_name="entity",
            name="collections",
        ),
        migrations.RemoveField(
            model_name="entity",
            name="data",
        ),
        migrations.RenameField(
            model_name="data",
            old_name="entity2",
            new_name="entity",
        ),
        migrations.AlterField(
            model_name="data",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="data",
                to="flow.Collection",
            ),
        ),
        migrations.AlterField(
            model_name="data",
            name="entity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="data",
                to="flow.Entity",
            ),
        ),
        migrations.AlterField(
            model_name="entity",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="flow.Collection",
            ),
        ),
    ]
