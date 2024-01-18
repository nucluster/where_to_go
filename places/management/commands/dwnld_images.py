from django.core.management.base import BaseCommand
from places.models import Image


class Command(BaseCommand):
    help = 'Download images'

    def handle(self, *args, **options):
        for img in Image.objects.all():
            img.download_image()
