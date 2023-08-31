# Generated by Django 4.2.1 on 2023-06-16 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0018_alter_formquestion_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formquestion',
            name='options',
        ),
        migrations.AddField(
            model_name='formquestion',
            name='options_type',
            field=models.IntegerField(choices=[(1, 'Single'), (2, 'Multiple')], default=None, null=True),
        ),
    ]