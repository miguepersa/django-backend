# Generated by Django 4.1 on 2023-08-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0071_alter_resource_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='program',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
