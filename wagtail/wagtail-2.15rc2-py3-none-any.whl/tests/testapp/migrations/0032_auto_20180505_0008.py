# Generated by Django 2.0.4 on 2018-05-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0031_customdocument_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='file_hash',
            field=models.CharField(blank=True, editable=False, max_length=40),
        ),
        migrations.AddField(
            model_name='customimagefilepath',
            name='file_hash',
            field=models.CharField(blank=True, editable=False, max_length=40),
        ),
    ]
