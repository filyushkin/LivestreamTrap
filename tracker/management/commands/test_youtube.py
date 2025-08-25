from django.core.management.base import BaseCommand
from tracker.youtube_service import get_channel_stats


class Command(BaseCommand):
    help = 'Test YouTube API connection'

    def add_arguments(self, parser):
        parser.add_argument('handle', type=str, help='YouTube channel handle')

    def handle(self, *args, **options):
        handle = options['handle']
        print(f"Testing channel: {handle}")

        data = get_channel_stats(handle)
        if data:
            print(f"Name: {data['name']}")
            print(f"Subscribers: {data['subscribers_count']}")
            print(f"Current streams: {data['current_streams_count']}")
            print(f"Channel ID: {data['channel_id']}")
        else:
            print("Channel not found or API error")
