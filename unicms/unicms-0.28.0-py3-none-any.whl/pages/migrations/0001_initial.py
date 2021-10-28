# Generated by Django 3.1.4 on 2021-01-15 11:24

import cms.medias.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from cms.templates.models import CMS_TEMPLATE_BLOCK_SECTIONS

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(max_length=1024)),
                ('image', models.ImageField(blank=True, max_length=512, null=True, upload_to='images/categories', validators=[cms.medias.validators.validate_file_extension, cms.medias.validators.validate_file_size])),
            ],
            options={
                'verbose_name_plural': 'Content Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('draft_of', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=160)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, help_text='Descriptionused for SEO.', null=True)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=33)),
                ('type', models.CharField(choices=[('standard', 'Page'), ('home', 'Home Page')], default='standard', max_length=33)),
            ],
            options={
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='PageBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=(lambda: CMS_TEMPLATE_BLOCK_SECTIONS)(),
                                             help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Block',
            },
        ),
        migrations.CreateModel(
            name='PageCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=(lambda: CMS_TEMPLATE_BLOCK_SECTIONS)(),
                             help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Carousel',
            },
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(help_text='url')),
            ],
            options={
                'verbose_name_plural': 'Page Links',
            },
        ),
        migrations.CreateModel(
            name='PageLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('title', models.CharField(max_length=256)),
                ('language', models.CharField(choices=(lambda: settings.LANGUAGES)(), default='en', max_length=12)),
            ],
            options={
                'verbose_name_plural': 'Page Localizations',
            },
        ),
        migrations.CreateModel(
            name='PageMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=(lambda: CMS_TEMPLATE_BLOCK_SECTIONS)(), 
                                             help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('url', models.URLField(blank=True, help_text='url', null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Medias',
            },
        ),
        migrations.CreateModel(
            name='PageMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=(lambda: CMS_TEMPLATE_BLOCK_SECTIONS)(), 
                                             help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Navigation Bars',
            },
        ),
        migrations.CreateModel(
            name='PageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_page', to='cmspages.page')),
                ('related_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_page', to='cmspages.page')),
            ],
            options={
                'verbose_name_plural': 'Related Pages',
            },
        ),
        migrations.CreateModel(
            name='PagePublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='container_page', to='cmspages.page')),
            ],
            options={
                'verbose_name_plural': 'Publication Contents',
            },
        ),
    ]
