# Generated by Django 5.0.2 on 2024-03-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_message_chat_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='room_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
