import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pytils.translit import slugify
from django.db.models import Q

from places.models import Image


class Command(BaseCommand):
    help = 'Download images'

    def handle(self, *args, **options):
        for image in Image.objects.filter(~Q(url=''), file=''):
            try:
                response = requests.get(image.url)
                response.raise_for_status()
                image_data = response.content
                image_file = ContentFile(image_data)
                image.file.save(
                    f'{slugify(image.place.title)}_{image.image_number}.jpg',
                    image_file, save=True)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Image successfully loaded and saved to {image.file.path}.')
                )
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.SUCCESS(f'Error downloading image: {e}')
                )
