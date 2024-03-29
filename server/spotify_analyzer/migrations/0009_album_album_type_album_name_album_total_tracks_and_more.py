# Generated by Django 4.2.6 on 2023-11-08 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_analyzer', '0008_alter_playlist_id_alter_user_liked_tracks'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_type',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='total_tracks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='url',
            field=models.TextField(null=True),
        ),
    ]
