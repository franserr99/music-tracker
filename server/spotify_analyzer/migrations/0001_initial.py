# Generated by Django 4.2.6 on 2023-10-16 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('uri', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('track_name', models.CharField(max_length=100)),
                ('track_artists', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Track',
            },
        ),
        migrations.CreateModel(
            name='TrackFeatures',
            fields=[
                ('track', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='features', serialize=False, to='spotify_analyzer.track')),
                ('danceability', models.FloatField()),
                ('energy', models.FloatField()),
                ('key', models.FloatField()),
                ('loudness', models.FloatField()),
                ('mode', models.FloatField()),
                ('speechiness', models.FloatField()),
                ('acousticness', models.FloatField()),
                ('instrumentalness', models.FloatField()),
                ('liveness', models.FloatField()),
                ('valence', models.FloatField()),
                ('tempo', models.FloatField()),
            ],
            options={
                'db_table': 'TrackFeatures',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('liked_tracks', models.ManyToManyField(related_name='liked_by_users', to='spotify_analyzer.track')),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('playlist_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists_created', to='spotify_analyzer.user')),
                ('liked_by', models.ManyToManyField(related_name='playlists_added', to='spotify_analyzer.user')),
                ('tracks', models.ManyToManyField(related_name='included_in_playlists', to='spotify_analyzer.track')),
            ],
            options={
                'db_table': 'Playlist',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recorded', models.DateTimeField()),
                ('relative_term', models.CharField(max_length=30)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_history', to='spotify_analyzer.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_history', to='spotify_analyzer.user')),
            ],
            options={
                'db_table': 'History',
            },
        ),
        migrations.AddConstraint(
            model_name='history',
            constraint=models.UniqueConstraint(fields=('user', 'relative_term', 'track', 'date_recorded'), name='unique_history'),
        ),
    ]
