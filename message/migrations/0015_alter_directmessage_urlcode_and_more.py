# Generated by Django 5.0.1 on 2024-08-06 01:43

import project.snowflake
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0014_alter_groupmessage_mentioned_user_and_more'),
    ]

    operations = [
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