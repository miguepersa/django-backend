# Generated by Django 4.1 on 2023-06-01 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content',
            field=models.CharField(max_length=100),
        ),
    ]
