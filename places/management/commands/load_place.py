import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from pytils.translit import slugify

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
            defaults = {
                'short_description': raw_place['description_short'],
                'long_description': raw_place['description_long'],
                'longitude': raw_place['coordinates']['lng'],
                'latitude': raw_place['coordinates']['lat'],
            }
            place, created = Place.objects.get_or_create(
                title=raw_place['title'],
                defaults=defaults
            )
            if created:
                for url in raw_place['imgs']:
                    image, _ = Image.objects.get_or_create(
                        url=url, place=place)
                    response = requests.get(url)
                    response.raise_for_status()
                    image_data = response.content
                    image_file = ContentFile(image_data)
                    image.file.save(
                        f'{slugify(place.title)}_{image.image_number}.jpg',
                        image_file, save=True)

                self.stdout.write(self.style.SUCCESS(
                    'JSON data and images successfully loaded and saved.'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'JSON data for place {place.title} has already been saved to the database.')
                )

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(
                f'Error downloading or decoding JSON: {e}'))
