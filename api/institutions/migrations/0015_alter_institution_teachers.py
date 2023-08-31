# Generated by Django 4.1 on 2023-05-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_employee_programs_remove_teacher_course'),
        ('institutions', '0014_alter_institution_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='teachers',
            field=models.ManyToManyField(blank=True, null=True, related_name='institution', to='users.teacher'),
        ),
    ]