# Generated by Django 4.1 on 2023-08-26 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0074_rename_learning_outcome_lesson_learning_outcomes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='type',
            field=models.CharField(choices=[('SCREENSHOT', 'Captura'), ('RESOURCE', 'Recurso'), ('PROGRAM', 'Programa')], default='RESOURCE', max_length=50),
        ),
    ]
