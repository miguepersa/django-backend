# Generated by Django 4.1 on 2023-08-26 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0073_alter_resource_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='learning_outcome',
            new_name='learning_outcomes',
        ),
    ]
