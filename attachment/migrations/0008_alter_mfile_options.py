# Generated by Django 5.0.1 on 2024-08-09 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0007_alter_mfile_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mfile',
            options={'ordering': ['urlCode']},
        ),
    ]