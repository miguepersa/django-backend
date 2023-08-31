# Generated by Django 4.2.1 on 2023-05-17 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0011_alter_lesson_program_coursesection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='program',
        ),
        migrations.CreateModel(
            name='LessonProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_numer', models.IntegerField(blank=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lesson_program', to='academic.lesson')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lesson_program', to='academic.program')),
            ],
        ),
    ]
