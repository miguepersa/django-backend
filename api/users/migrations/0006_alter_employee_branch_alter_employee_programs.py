# Generated by Django 4.2 on 2023-04-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
        ('users', '0005_employee_user_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.CharField(max_length=64,choices=[('CCS', 'Caracas'), ('MCB', 'Maracaibo'), ('PLC', 'Puerto la Cruz')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='programs',
            field=models.ManyToManyField(blank=True, related_name='employees', to='academic.program'),
        ),
    ]
