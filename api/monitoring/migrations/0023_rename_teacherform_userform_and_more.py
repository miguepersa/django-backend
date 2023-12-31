# Generated by Django 4.2.1 on 2023-07-06 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0024_alter_institutionlevel_student_sections_and_more'),
        ('users', '0018_remove_employee_programs_remove_teacher_course'),
        ('monitoring', '0022_rename_current_lesson_classjournal_lesson'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeacherForm',
            new_name='UserForm',
        ),
        migrations.RenameModel(
            old_name='TeacherFormAnswer',
            new_name='UserFormAnswer',
        ),
        migrations.RemoveField(
            model_name='userform',
            name='teacher_profile',
        ),
        migrations.AddField(
            model_name='userform',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='forms', to=settings.AUTH_USER_MODEL),
        ),
    ]
