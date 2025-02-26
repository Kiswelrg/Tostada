# Generated by Django 5.0.1 on 2024-07-26 07:40

import project.snowflake
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0008_remove_directmessage_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directmessage',
            name='id',
        ),
        migrations.RemoveField(
            model_name='groupmessage',
            name='id',
        ),
        migrations.AlterField(
            model_name='directmessage',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=project.snowflake.getMessageMessageSnowflakeID, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='groupmessage',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=project.snowflake.getMessageMessageSnowflakeID, primary_key=True, serialize=False, unique=True),
        ),
    ]
