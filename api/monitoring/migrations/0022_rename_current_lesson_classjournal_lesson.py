# Generated by Django 4.2.1 on 2023-06-22 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0021_alter_formquestion_options_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classjournal',
            old_name='current_lesson',
            new_name='lesson',
        ),
    ]
