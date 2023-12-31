# Generated by Django 4.2.1 on 2023-05-18 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_employee_programs_remove_teacher_course'),
        ('academic', '0016_alter_course_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(blank=True, related_name='courses', to='users.teacher'),
        ),
        migrations.AlterField(
            model_name='program',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='programs', to='users.employee'),
        ),
    ]
