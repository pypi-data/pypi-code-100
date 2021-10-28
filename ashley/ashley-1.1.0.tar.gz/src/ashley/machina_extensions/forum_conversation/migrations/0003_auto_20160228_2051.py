# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 19:51
from __future__ import unicode_literals

import machina.core.validators
import machina.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("forum_conversation", "0002_post_anonymous_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=machina.models.fields.MarkupTextField(
                no_rendered_field=True,
                validators=[machina.core.validators.NullableMaxLengthValidator(None)],
                verbose_name="Content",
            ),
        ),
    ]
