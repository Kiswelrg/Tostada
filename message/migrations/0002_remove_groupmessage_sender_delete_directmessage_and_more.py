# Generated by Django 5.0.1 on 2024-04-29 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmessage',
            name='sender',
        ),
        migrations.DeleteModel(
            name='DirectMessage',
        ),
        migrations.DeleteModel(
            name='GroupMessage',
        ),
    ]