# Generated by Django 5.1.1 on 2025-07-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0024_remove_chatmessage_mentioned_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='content_text',
            field=models.TextField(blank=True, db_index=True, max_length=4000),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='has_attachment',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='has_link',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='has_mention',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='has_text',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='mention_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
