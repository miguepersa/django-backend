# Generated by Django 4.1 on 2023-05-04 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0002_resource_lesson_resources'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=45)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('title', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=128)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forums', to='academic.course')),
                ('members', models.ManyToManyField(related_name='forums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachments', models.FileField(upload_to='')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopicMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=45)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=45)),
                ('attachments', models.FileField(upload_to='')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_messages', to=settings.AUTH_USER_MODEL)),
                ('previous_version', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_version', to='forums.topicmessage')),
                ('responds_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='forums.topicmessage')),
            ],
        ),
        migrations.CreateModel(
            name='ForumTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed'), ('HIDDEN', 'Hidden')], max_length=32)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True)),
                ('forum_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_topics', to='forums.forum')),
                ('lesson_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_topics', to='academic.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='ForumMessageReadBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1024)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('REQUEST', 'Request'), ('INFO', 'Info'), ('REPORT', 'Report'), ('QUESTION', 'Question')], max_length=32)),
                ('message_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='read_by', to='forums.forummessage')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='read_forum_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='forummessage',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='forums.forumtopic'),
        ),
    ]
