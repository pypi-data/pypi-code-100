# Generated by Django 3.1.7 on 2021-10-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mad_notifications', '0003_auto_20211019_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
