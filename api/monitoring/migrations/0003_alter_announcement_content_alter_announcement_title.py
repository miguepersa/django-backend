# Generated by Django 4.2.1 on 2023-05-23 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_alter_announcement_image_alter_announcement_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='content',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]