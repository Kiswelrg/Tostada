# Generated by Django 5.0.1 on 2024-07-26 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0011_remove_channelofchat_server_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channelofchat',
            old_name='server_placeholder',
            new_name='server',
        ),
        migrations.RenameField(
            model_name='channelofvoice',
            old_name='server_placeholder',
            new_name='server',
        ),
    ]
