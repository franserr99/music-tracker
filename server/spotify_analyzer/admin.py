from django.contrib import admin
from .models import Track, TrackFeatures, History, User, Playlist


# Register the Track model
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('uri', 'track_name', 'track_artists')
    search_fields = ('uri', 'track_name', 'track_artists')


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
    list_display = ('playlist_id', 'created_by')
    search_fields = ('playlist_id', 'created_by__id')
