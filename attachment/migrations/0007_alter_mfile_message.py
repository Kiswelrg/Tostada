# Generated by Django 5.0.1 on 2024-08-09 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0006_rename_gmfile_mfile'),
        ('message', '0019_rename_groupmessage_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mfile',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='message.chatmessage'),
        ),
    ]
