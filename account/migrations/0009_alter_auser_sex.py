# Generated by Django 5.0.1 on 2024-05-01 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_auser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auser',
            name='sex',
            field=models.CharField(choices=[('1', '女'), ('0', '男'), ('2', '0b01')], default='2', max_length=2),
        ),
    ]