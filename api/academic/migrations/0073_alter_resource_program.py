# Generated by Django 4.1 on 2023-08-26 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0072_alter_resource_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.program'),
        ),
    ]
