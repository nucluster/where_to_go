import json
import os
from django.core.management.base import BaseCommand
from places.models import Place, Image


def read_json_from_folder(folder_path):
    json_data = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path) and filename.endswith('.json'):
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    json_data.append(data)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON in the file {filename}: {e}')
    return json_data


class Command(BaseCommand):
    help = 'Load JSON data from folder path and save it to the database'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='URL of the JSON file')

    def handle(self, *args, **options):
        folder = options['folder']
        json_data_list = read_json_from_folder(folder)
        for index, json_data in enumerate(json_data_list, start=1):
            place = Place.objects.get_or_create(
                title=json_data['title'],
                description_short=json_data['description_short'],
                description_long=json_data['description_long'],
                longitude=json_data['coordinates']['lng'],
                latitude=json_data['coordinates']['lat'],
            )
            if place[1]:
                [Image.objects.get_or_create(
                    url=url, place=place[0]) for url in json_data['imgs']]

                self.stdout.write(self.style.SUCCESS(
                    f'Place {index} {place[0].title} JSON data successfully loaded and saved to the database.'))

            else:
                self.stdout.write(self.style.SUCCESS(
                    f'JSON data for place {index} {place[0].title} has already been saved to the database.'))
