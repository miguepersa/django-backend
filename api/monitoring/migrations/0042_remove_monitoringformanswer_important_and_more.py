# Generated by Django 4.2.1 on 2023-08-22 18:25

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0041_trainingtask_reviewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoringformanswer',
            name='important',
        ),
        migrations.AlterField(
            model_name='monitoringform',
            name='comments',
            field=models.CharField(blank=True, max_length=2048),
        ),
        migrations.AlterField(
            model_name='monitoringform',
            name='feedback',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='monitoringformanswer',
            name='comment',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='trainingtask',
            name='file',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='raw/'),
        ),
    ]
