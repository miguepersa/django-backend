# Generated by Django 4.2.1 on 2023-07-07 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0051_classschedule'),
        ('monitoring', '0028_alter_formtemplate_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formquestion',
            name='program',
        ),
        migrations.AddField(
            model_name='formquestion',
            name='licenss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='form_questions', to='academic.license'),
        ),
    ]
