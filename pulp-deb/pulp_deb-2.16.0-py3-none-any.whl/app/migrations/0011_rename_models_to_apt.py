# Generated by Django 2.2.13 on 2020-06-10 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deb', '0010_debpublication_signing_service'),
    ]

    operations = [
        migrations.RenameModel('DebDistribution', 'AptDistribution'),
        migrations.RenameModel('DebPublication', 'AptPublication'),
        migrations.RenameModel('DebRemote', 'AptRemote'),
        migrations.RenameModel('DebRepository', 'AptRepository'),
        migrations.AlterField(
            model_name='aptdistribution',
            name='basedistribution_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name='deb_aptdistribution',
                serialize=False,
                to='core.BaseDistribution',
            ),
        ),
        migrations.AlterField(
            model_name='aptdistribution',
            name='publication',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='deb_aptdistribution',
                to='core.Publication',
            ),
        ),
        migrations.AlterField(
            model_name='aptpublication',
            name='publication_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name='deb_aptpublication',
                serialize=False,
                to='core.Publication',
            ),
        ),
        migrations.AlterField(
            model_name='aptpublication',
            name='signing_service',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='deb_aptpublication',
                to='deb.AptReleaseSigningService',
            ),
        ),
        migrations.AlterField(
            model_name='aptremote',
            name='remote_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name='deb_aptremote',
                serialize=False,
                to='core.Remote',
            ),
        ),
        migrations.AlterField(
            model_name='aptrepository',
            name='repository_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name='deb_aptrepository',
                serialize=False,
                to='core.Repository',
            ),
        ),
    ]
