# Generated by Django 4.2.6 on 2023-11-04 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_analyzer', '0002_user_access_token_user_refresh_token_user_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_token',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
