# Generated by Django 5.0.1 on 2024-05-01 15:55

import tool.util.model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_categoryinserver_urlcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryinserver',
            name='urlCode',
            field=models.PositiveBigIntegerField(db_index=True, default=tool.util.model.getCategoryCode, unique=True),
        ),
    ]