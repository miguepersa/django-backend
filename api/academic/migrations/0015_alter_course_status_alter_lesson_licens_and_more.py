# Generated by Django 4.2.1 on 2023-05-18 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0014_remove_course_institution_level_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(max_length=16, choices=[('CREATED', 'Creado'), ('SUSPENDED', 'Suspendido'), (
                'ACTIVE', 'Activo'), ('INACTIVE', 'Inactivo'), ('FINISHED', 'Finalizado')], default='CREATED'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='licens',
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name='License'),
        ),
        migrations.AlterField(
            model_name='program',
            name='lic',
            field=models.CharField(max_length=255, verbose_name='License'),
        ),
    ]
