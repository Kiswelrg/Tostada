# Generated by Django 5.0.1 on 2024-08-09 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_delete_buser'),
        ('message', '0018_remove_groupmessage_id_alter_groupmessage_urlcode'),
        ('tool', '0033_channelofchat_is_dm'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GroupMessage',
            new_name='ChatMessage',
        ),
    ]