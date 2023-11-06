# Generated by Django 4.2.6 on 2023-11-05 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_analyzer', '0005_artist_genre_remove_track_track_artists_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='uri',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artist_images', to='spotify_analyzer.artist'),
        ),
        migrations.AlterField(
            model_name='track',
            name='track_artists',
            field=models.ManyToManyField(related_name='track_catalogue', to='spotify_analyzer.artist'),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('uri', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('artists', models.ManyToManyField(related_name='album_catalogue', to='spotify_analyzer.artist')),
                ('tracks', models.ManyToManyField(related_name='appears_in', to='spotify_analyzer.track')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album_images', to='spotify_analyzer.album'),
        ),
    ]