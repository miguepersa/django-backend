# Generated by Django 4.2.1 on 2023-07-12 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0052_alter_classschedule_course_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesection',
            name='next_lesson',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.lesson'),
        ),
    ]
