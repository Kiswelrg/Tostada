# Generated by Django 5.0.1 on 2024-07-12 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_remove_auser_sex'),
        ('tool', '0007_alter_channelofio_category_alter_channelofio_server_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChannelOfIO',
            new_name='ChannelOfChat',
        ),
        migrations.RenameModel(
            old_name='UserChannelOfIORole',
            new_name='UserChannelOfChatRole',
        ),
    ]
