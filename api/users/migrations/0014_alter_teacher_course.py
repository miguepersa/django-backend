# Generated by Django 4.2.1 on 2023-05-15 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0004_rename_program_id_course_program_alter_course_status'),
        ('users', '0013_remove_employee_role_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='course',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to='academic.course'),
        ),
    ]
