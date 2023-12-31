# Generated by Django 4.2.1 on 2023-07-06 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitoring', '0023_rename_teacherform_userform_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userformanswer',
            name='teacher',
        ),
        migrations.AddField(
            model_name='userformanswer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_form_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userformanswer',
            name='form_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_form_answers', to='monitoring.formtemplate'),
        ),
    ]
