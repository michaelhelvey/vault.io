# Generated by Django 2.0.2 on 2018-03-05 00:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
