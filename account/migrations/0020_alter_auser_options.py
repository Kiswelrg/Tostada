# Generated by Django 5.0.1 on 2024-08-09 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_delete_buser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auser',
            options={'ordering': ['urlCode']},
        ),
    ]
