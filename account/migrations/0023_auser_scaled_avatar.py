# Generated by Django 5.1.1 on 2024-10-22 07:39

import UtilGlobal.validator.FieldFile
import account.models
import media.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_alter_auser_avatar_alter_auser_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='auser',
            name='scaled_avatar',
            field=models.ImageField(blank=True, default='', storage=media.models.MediaFileSystemStorage, upload_to=account.models.AUser.scaled_avatar_dir_path, validators=[UtilGlobal.validator.FieldFile.imagefile_validator]),
        ),
    ]