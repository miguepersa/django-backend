# Generated by Django 4.2.1 on 2023-05-15 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_announcement_announcementuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forum',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='forummessagereadby',
            old_name='message_id',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='forummessagereadby',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='forumtopic',
            old_name='forum_id',
            new_name='forum',
        ),
        migrations.RenameField(
            model_name='forumtopic',
            old_name='lesson_id',
            new_name='lesson',
        ),
    ]
