# Generated by Django 4.1 on 2023-05-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0008_alter_topicmessage_attachments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumtopic',
            name='description',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
