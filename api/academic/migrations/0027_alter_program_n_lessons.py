# Generated by Django 4.1 on 2023-05-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0026_course_academic_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='n_lessons',
            field=models.IntegerField(blank=True, default=30, null=True),
        ),
    ]
