# Generated by Django 4.1 on 2023-06-22 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0020_forumtopic_last_interaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicmessage',
            old_name='attachments',
            new_name='attachment',
        ),
    ]
