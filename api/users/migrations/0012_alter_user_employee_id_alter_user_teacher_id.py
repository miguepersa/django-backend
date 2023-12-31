# Generated by Django 4.2.1 on 2023-05-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employee_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_id', to='users.employee'),
        ),
        migrations.AlterField(
            model_name='user',
            name='teacher_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_id', to='users.teacher'),
        ),
    ]
