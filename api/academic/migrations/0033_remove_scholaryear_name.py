# Generated by Django 4.1 on 2023-05-26 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0032_scholaryear_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholaryear',
            name='name',
        ),
    ]
