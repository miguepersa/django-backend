# Generated by Django 4.1 on 2023-05-29 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0035_academicyear_alter_course_academic_year_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='academic_year',
            new_name='year',
        ),
    ]
