from django.contrib import admin
from .models import Track, TrackFeatures, History, User, Playlist
from .models import Genre, Image, Artist, Album


# Register the Track model
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('uri', 'track_name', 'get_artists')
    # Allows searching by artist name
    search_fields = ('uri', 'track_name', 'track_artists__name')

    def get_artists(self, obj):
        # This method fetches all related artists
        # and joins their names into a single string.
        return ", ".join([artist.name for artist in obj.track_artists.all()])
    # Sets the column header in the admin list view
    get_artists.short_description = 'Artists'


# Register the TrackFeatures model
@admin.register(TrackFeatures)
class TrackFeaturesAdmin(admin.ModelAdmin):
    list_display = ('track', 'danceability', 'energy', 'tempo')
    search_fields = ('track__uri',)


# Register the History model
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_recorded', 'relative_term', 'track')
    search_fields = ('user__id', 'relative_term', 'track__uri')


# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)


# Register the Playlist model
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by')
    search_fields = ('id', 'created_by__id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('uri', 'name', 'get_genres')
    search_fields = ('uri', 'name', 'genres__name')
    # Allows searching by genre name

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'height', 'width', 'artist',
                    'album')  # Fields to display
    search_fields = ('artist__name', 'album__name')  # Fields to search
    list_filter = ('artist', 'album')  # Filters to be added in the sidebar

    # def artist_name(self, obj):
    #     return obj.artist.name
    # artist_name.short_description = 'Artist Name'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('uri', 'name', 'album_type', 'total_tracks', 'url')
    # Fields to search in the admin
    search_fields = ('name', 'artists__name', 'tracks__name')
    # A nicer widget for ManyToMany fields
    filter_horizontal = ('artists', 'tracks')
