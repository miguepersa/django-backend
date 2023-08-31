# Generated by Django 4.2.1 on 2023-05-16 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_alter_course_group_numbers_alter_course_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forums', '0003_rename_course_id_forum_course_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ForumMessageReadBy',
            new_name='TopicMessageReadBy',
        ),
        migrations.RenameField(
            model_name='topicmessage',
            old_name='creation_date',
            new_name='date',
        ),
        migrations.AddField(
            model_name='topicmessage',
            name='text',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='topicmessage',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_messages', to='forums.forumtopic'),
        ),
        migrations.AlterField(
            model_name='forumtopic',
            name='description',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='forumtopic',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_topics', to='academic.lesson'),
        ),
        migrations.AlterField(
            model_name='topicmessage',
            name='type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='topicmessagereadby',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='read_by', to='forums.topicmessage'),
        ),
        migrations.DeleteModel(
            name='ForumMessage',
        ),
    ]
