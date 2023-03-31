# Generated by Django 4.1.7 on 2023-03-24 10:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]