# Generated by Django 4.2.1 on 2023-07-12 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0053_coursesection_next_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonprogram',
            name='next_lesson',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_lesson', to='academic.lessonprogram'),
        ),
    ]
