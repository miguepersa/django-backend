# Generated by Django 4.1 on 2023-05-22 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0013_remove_institutionlevel_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='logo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
