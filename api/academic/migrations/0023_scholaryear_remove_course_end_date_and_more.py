# Generated by Django 4.2.1 on 2023-05-22 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0022_alter_lesson_resources'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScholarYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='scholar_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='academic.scholaryear'),
        ),
    ]
