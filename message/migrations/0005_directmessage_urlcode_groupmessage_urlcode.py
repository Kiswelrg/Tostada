# Generated by Django 5.0.1 on 2024-07-21 07:24

import message.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_alter_directmessage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessage',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=message.util.getDirectMessageCode, null=True),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=message.util.getGroupMessageCode, null=True),
        ),
    ]