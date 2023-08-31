# Generated by Django 4.1 on 2023-05-22 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0022_alter_lesson_resources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='course_outline',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='n_lessons',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='planification_term1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='planification_term2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='planification_term3',
            field=models.URLField(blank=True, null=True),
        ),
    ]