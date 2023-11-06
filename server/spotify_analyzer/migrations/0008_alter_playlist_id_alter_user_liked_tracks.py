# Generated by Django 4.2.6 on 2023-11-05 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_analyzer', '0007_rename_playlist_id_playlist_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_tracks',
            field=models.ManyToManyField(related_name='users_liked', to='spotify_analyzer.track'),
        ),
    ]
