# Generated by Django 5.1 on 2024-09-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0034_alter_channelofchat_options_alter_server_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverrole',
            name='auth',
        ),
        migrations.AlterField(
            model_name='serverrole',
            name='auth_value',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
