# Generated by Django 5.0.1 on 2024-05-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_auser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auser',
            name='sex',
            field=models.CharField(choices=[('0', '男'), ('2', '0b01'), ('1', '女')], default='2', max_length=2),
        ),
    ]