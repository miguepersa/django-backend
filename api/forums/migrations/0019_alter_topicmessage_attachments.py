# Generated by Django 4.1 on 2023-06-20 02:32

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0018_remove_topicmessagereadby_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmessage',
            name='attachments',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='raw/'),
        ),
    ]
