# Generated by Django 4.2.1 on 2023-08-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0026_institution_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(blank=True, choices=[('A', 'Tipo A'), ('B', 'Tipo B'), ('C', 'Tipo C')], max_length=8, null=True),
        ),
    ]
