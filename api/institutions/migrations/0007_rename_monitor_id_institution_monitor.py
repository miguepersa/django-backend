# Generated by Django 4.2.1 on 2023-05-15 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_rename_students_per_classwoom_institution_students_per_classroom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institution',
            old_name='monitor_id',
            new_name='monitor',
        ),
    ]