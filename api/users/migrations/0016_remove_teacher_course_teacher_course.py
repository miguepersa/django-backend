# Generated by Django 4.2.1 on 2023-05-15 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_alter_course_group_numbers_alter_course_status'),
        ('users', '0015_rename_employee_id_user_employee_profile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='course',
        ),
        migrations.AddField(
            model_name='teacher',
            name='course',
            field=models.ManyToManyField(blank=True, related_name='teacher', to='academic.course'),
        ),
    ]
