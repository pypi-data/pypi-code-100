# Generated by Django 2.1.5 on 2019-03-05 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_templates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ['name'], 'verbose_name': 'Template', 'verbose_name_plural': 'Templates'},
        ),
    ]
