# Generated by Django 4.2.1 on 2023-06-28 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0047_alter_program_lic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='lic',
            new_name='licenss',
        ),
    ]