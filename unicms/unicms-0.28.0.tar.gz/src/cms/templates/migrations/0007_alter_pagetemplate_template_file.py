# Generated by Django 3.2.5 on 2021-07-19 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmstemplates', '0006_alter_pagetemplate_template_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetemplate',
            name='template_file',
            field=models.CharField(choices=[('publication_view_hero_original.html', 'publication_view_hero_original.html'), ('unical_center_top_ab_a_double.html', 'unical_center_top_ab_a_double.html'), ('department_demacs.html', 'department_demacs.html'), ('department.html', 'department.html'), ('department_ctc.html', 'department_ctc.html'), ('publication_view.html', 'publication_view.html'), ('department_diam.html', 'department_diam.html'), ('department_dinci.html', 'department_dinci.html'), ('portale_home_dipartimento_v3.html', 'portale_home_dipartimento_v3.html'), ('unical_main_center_alternative.html', 'unical_main_center_alternative.html'), ('unical.html', 'unical.html'), ('department_dimeg.html', 'department_dimeg.html'), ('portale_home_v_original.html', 'portale_home_v_original.html'), ('department_dispes.html', 'department_dispes.html'), ('department_dimes.html', 'department_dimes.html'), ('department_disu.html', 'department_disu.html'), ('unical_right_spaced.html', 'unical_right_spaced.html'), ('publication_list.html', 'publication_list.html'), ('portale_home_dipartimento_v3_dimes.html', 'portale_home_dipartimento_v3_dimes.html'), ('department_dfssn.html', 'department_dfssn.html'), ('department_desf.html', 'department_desf.html'), ('department_discag.html', 'department_discag.html'), ('department_dices.html', 'department_dices.html'), ('department_dibest.html', 'department_dibest.html'), ('italia.html', 'italia.html'), ('department_fis.html', 'department_fis.html')], max_length=1024),
        ),
    ]
