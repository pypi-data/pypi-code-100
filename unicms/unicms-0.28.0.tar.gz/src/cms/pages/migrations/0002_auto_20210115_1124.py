# Generated by Django 3.1.4 on 2021-01-15 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmspublications', '0001_initial'),
        ('cmstemplates', '0001_initial'),
        ('cmsmedias', '0001_initial'),
        ('cmscontexts', '0001_initial'),
        ('cmsmenus', '0002_auto_20210115_1124'),
        ('cmspages', '0001_initial'),
        ('cmscarousels', '0002_auto_20210115_1124'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pagepublication',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publication_content', to='cmspublications.publication'),
        ),
        migrations.AddField(
            model_name='pagemenu',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsmenus.navigationbar'),
        ),
        migrations.AddField(
            model_name='pagemenu',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='pagemedia',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsmedias.media'),
        ),
        migrations.AddField(
            model_name='pagemedia',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='pagelocalization',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagelocalization_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pagelocalization',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagelocalization_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pagelocalization',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='pagelink',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='pagecarousel',
            name='carousel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmscarousels.carousel'),
        ),
        migrations.AddField(
            model_name='pagecarousel',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='pageblock',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmstemplates.templateblock'),
        ),
        migrations.AddField(
            model_name='pageblock',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmspages.page'),
        ),
        migrations.AddField(
            model_name='page',
            name='base_template',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='cmstemplates.pagetemplate'),
        ),
        migrations.AddField(
            model_name='page',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='page',
            name='webpath',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='cmscontexts.webpath'),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='pagerelated',
            unique_together={('page', 'related_page')},
        ),
    ]
