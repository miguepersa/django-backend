# Generated by Django 4.2.1 on 2023-07-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_remove_room_label_alter_room_name_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
