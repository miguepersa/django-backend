# Generated by Django 4.2.1 on 2023-07-06 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0027_merge_20230706_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formtemplate',
            name='status',
            field=models.CharField(choices=[('Borrador', 'Borrador'), ('Enviado', '')], default='Borrador', max_length=128),
        ),
    ]
