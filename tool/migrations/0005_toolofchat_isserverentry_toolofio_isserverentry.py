# Generated by Django 5.0.1 on 2024-05-02 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_alter_categoryinserver_urlcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelofchat',
            name='isServerEntry',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='channelofio',
            name='isServerEntry',
            field=models.BooleanField(default=False),
        ),
    ]