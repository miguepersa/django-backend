# Generated by Django 4.1 on 2023-05-30 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0010_alter_forumtopic_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicmessage',
            name='previous_version',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_version', to='forums.topicmessage'),
        ),
        migrations.AlterField(
            model_name='topicmessage',
            name='responds_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='forums.topicmessage'),
        ),
    ]