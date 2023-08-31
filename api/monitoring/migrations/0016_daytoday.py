# Generated by Django 4.2.1 on 2023-06-12 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0038_rename_teacher_course_teachers'),
        ('monitoring', '0015_remove_announcementuser_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayToDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('current_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='academic.lesson')),
            ],
        ),
    ]