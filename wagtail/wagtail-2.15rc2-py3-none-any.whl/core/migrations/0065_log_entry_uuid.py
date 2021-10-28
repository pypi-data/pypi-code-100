# Generated by Django 3.2.5 on 2021-09-01 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0064_log_timestamp_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='modellogentry',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, help_text='Log entries that happened as part of the same user action are assigned the same UUID', null=True),
        ),
        migrations.AddField(
            model_name='pagelogentry',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, help_text='Log entries that happened as part of the same user action are assigned the same UUID', null=True),
        ),
    ]
