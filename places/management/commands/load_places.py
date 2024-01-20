import json
import os

from django.core.management.base import BaseCommand

from places.models import Image, Place


def read_json_from_folder(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path) and filename.endswith('.json'):
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    files.append(data)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON in the file {filename}: {e}')
    return files


class Command(BaseCommand):
    help = 'Load JSON data from folder path and save it to the database'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='URL of the JSON file')

    def handle(self, *args, **options):
        folder = options['folder']
        places = read_json_from_folder(folder)
        for index, raw_place in enumerate(places, start=1):
            place, created = Place.objects.get_or_create(
                title=raw_place['title'],
                description_short=raw_place['description_short'],
                description_long=raw_place['description_long'],
                longitude=raw_place['coordinates']['lng'],
                latitude=raw_place['coordinates']['lat'],
            )
            if created:
                [Image.objects.get_or_create(
                    url=url, place=place) for url in place['imgs']]

                self.stdout.write(self.style.SUCCESS(
                    f'Place {index} {raw_place[0].title} JSON data successfully loaded and saved to the database.'))

            else:
                self.stdout.write(self.style.SUCCESS(
                    f'JSON data for place {index} {raw_place[0].title} has already been saved to the database.'))
