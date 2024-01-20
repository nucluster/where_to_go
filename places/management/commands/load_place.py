import requests
from django.core.management.base import BaseCommand

from places.models import Image, Place


class Command(BaseCommand):
    help = 'Load JSON data from a URL and save it to the database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL of the JSON file')

    def handle(self, *args, **options):
        url = options['url']

        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_place = response.json()
            place = Place.objects.get_or_create(
                title=raw_place['title'],
                description_short=raw_place['short_description'],
                description_long=raw_place['long_description'],
                longitude=raw_place['coordinates']['lng'],
                latitude=raw_place['coordinates']['lat'],
            )
            [Image.objects.get_or_create(
                url=url, place=place[0]) for url in raw_place['imgs']]

            self.stdout.write(self.style.SUCCESS(
                'JSON data successfully loaded and saved to the database.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(
                f'Error downloading or decoding JSON: {e}'))
