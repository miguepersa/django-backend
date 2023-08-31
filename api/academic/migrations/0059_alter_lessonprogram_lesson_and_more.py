# Generated by Django 4.2.1 on 2023-08-09 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0058_alter_curricularcontent_component_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonprogram',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_program', to='academic.lesson'),
        ),
        migrations.AlterField(
            model_name='lessonprogram',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_program', to='academic.program'),
        ),
    ]