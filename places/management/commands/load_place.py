from django.core.management.base import BaseCommand
import requests
from pprint import pprint
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Load JSON data from a URL and save it to the database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL of the JSON file')

    def handle(self, *args, **options):
        url = options['url']

        try:
            # Загрузка JSON с указанного URL
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок при запросе

            # Преобразование JSON в словарь
            json_data = response.json()
            pprint(json_data)

            # Сохранение данных в базу данных
            # Создание экземпляра
            place = Place.objects.get_or_create(
                title=json_data['title'],
                description_short=json_data['description_short'],
                description_long=json_data['description_long'],
                longitude=json_data['coordinates']['lng'],
                latitude=json_data['coordinates']['lat'],
            )
            print(place)
            [Image.objects.get_or_create(
                url=url, place=place[0]) for url in json_data['imgs']]

            self.stdout.write(self.style.SUCCESS(
                'JSON data successfully loaded and saved to the database.'))

            for img in Image.objects.all():
                img.download_image()

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(
                f'Error downloading or decoding JSON: {e}'))
