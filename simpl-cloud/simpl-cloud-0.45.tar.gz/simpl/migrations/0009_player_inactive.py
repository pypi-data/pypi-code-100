# Generated by Django 3.2.5 on 2021-07-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpl', '0008_merge_20210727_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='inactive',
            field=models.BooleanField(default=False),
        ),
    ]
