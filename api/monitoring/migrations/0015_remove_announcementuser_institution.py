# Generated by Django 4.1 on 2023-06-12 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0014_announcementuser_institution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcementuser',
            name='institution',
        ),
    ]
