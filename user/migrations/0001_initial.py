# Generated by Django 5.0.1 on 2024-02-02 08:45

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='some_user', max_length=20)),
                ('username', models.CharField(db_index=True, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Enter a valid username', regex='^(?=.{6,20}$)(?![_0-9])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$')])),
                ('password', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Enter a valid username', regex='^.{6,48}$')])),
                ('sex', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('age', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('date_add', models.DateTimeField(default=django.utils.timezone.now)),
                ('info', models.FileField(blank=True, default=None, null=True, upload_to='')),
                ('additional', models.JSONField()),
            ],
        ),
    ]