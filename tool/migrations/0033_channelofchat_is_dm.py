# Generated by Django 5.0.1 on 2024-08-09 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0032_remove_userserverrole_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelofchat',
            name='is_dm',
            field=models.BooleanField(default=False),
        ),
    ]
