# Generated by Django 4.2.1 on 2023-08-29 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_alter_readroommessage_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='lesson_id',
        ),
    ]
