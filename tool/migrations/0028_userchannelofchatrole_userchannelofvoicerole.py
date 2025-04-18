# Generated by Django 5.0.1 on 2024-07-26 09:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_remove_auser_sex'),
        ('tool', '0027_remove_channelofchat_id_remove_channelofvoice_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChannelOfChatRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofchat_auths', to='tool.channelofchat')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofchat_auths', to='tool.serverrole', verbose_name='user role in the server')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofchat_auths', to='account.auser')),
            ],
        ),
        migrations.CreateModel(
            name='UserChannelOfVoiceRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofvoice_auths', to='tool.channelofvoice')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofvoice_auths', to='tool.serverrole', verbose_name='user role in the server')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channelofvoice_auths', to='account.auser')),
            ],
        ),
    ]
