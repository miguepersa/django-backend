# Generated by Django 4.1 on 2023-08-26 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0075_resource_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_goal',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
