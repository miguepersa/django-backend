# Generated by Django 4.2.1 on 2023-08-07 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0055_alter_coursesection_next_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonprogram',
            name='next_lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_lesson', to='academic.lessonprogram'),
        ),
    ]
