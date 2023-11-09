# Generated by Django 4.2.6 on 2023-11-05 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_analyzer', '0004_user_expires_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('uri', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='track',
            name='track_artists',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('url', models.TextField(primary_key=True, serialize=False)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='spotify_analyzer.artist')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(related_name='member_artists', to='spotify_analyzer.genre'),
        ),
        migrations.AddField(
            model_name='track',
            name='track_artists',
            field=models.ManyToManyField(related_name='artist_catalogue', to='spotify_analyzer.artist'),
        ),
    ]
