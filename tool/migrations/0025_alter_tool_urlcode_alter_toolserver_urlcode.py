# Generated by Django 5.0.1 on 2024-03-18 08:54

import tool.util.model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0024_categoryinserver_type_alter_tool_additional_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=tool.util.model.getToolCode, unique=True),
        ),
        migrations.AlterField(
            model_name='toolserver',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=tool.util.model.getToolServerCode, unique=True),
        ),
    ]