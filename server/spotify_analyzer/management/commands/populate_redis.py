from django.core.management.base import BaseCommand
from ...util.redis_util import from_db_to_redis, \
    get_redis_instance, get_data_from_redis


class Command(BaseCommand):
    help = 'Populates the Redis cache with data from\
    the database and retrieves it'

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate Redis cache...")
        success = from_db_to_redis()
        if success:
            self.stdout.write(self.style.SUCCESS(
                'Successfully populated Redis cache'))

            # Fetch data from Redis and print it
            r = get_redis_instance()
            if r:
                redis_data = get_data_from_redis(r)
                self.stdout.write("Redis Data:")
                self.stdout.write(f"Album URIs: {redis_data['albums']}")
                self.stdout.write(f"Artist URIs: {redis_data['artists']}")
                self.stdout.write(f"Playlist IDs: {redis_data['playlists']}")
                self.stdout.write(f"Track URIs: {redis_data['tracks']}")
            else:
                self.stdout.write(self.style.ERROR(
                    'Failed to create Redis instance'))
        else:
            self.stdout.write(self.style.ERROR(
                'Failed to populate Redis cache'))
