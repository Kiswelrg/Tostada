# Generated by Django 5.0.1 on 2024-07-26 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0023_remove_channelofchat_category_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategoryInServer',
        ),
    ]
