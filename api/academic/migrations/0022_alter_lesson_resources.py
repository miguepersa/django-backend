# Generated by Django 4.1 on 2023-05-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0021_alter_lesson_reference_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='resources',
            field=models.ManyToManyField(blank=True, related_name='resource_of', to='academic.resource'),
        ),
    ]