# Generated by Django 5.0.1 on 2024-03-18 07:02

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to=user.models.User.cover_dir_path),
        ),
        migrations.AddField(
            model_name='user',
            name='logo',
            field=models.ImageField(blank=True, default='', upload_to=user.models.User.avatar_dir_path),
        ),
    ]