import requests
from django.db import models
from django.core.files.base import ContentFile
from pytils.translit import slugify


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название места')
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['-id']

    def __str__(self):
        return self.title

    @property
    def coordinates(self):
        return {'lng': str(self.longitude), 'lat': str(self.latitude)}


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='places/',
                             verbose_name='Файл', blank=True)
    url = models.URLField(blank=True, verbose_name='Внешний URL')
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Позиция'
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['my_order']

    @property
    def get_url(self):
        if not self.file:
            return self.url
        return self.file.url

    def __str__(self):
        return f'{self.id} {self.place.title}'

    def download_image(self):
        if self.url and not self.file:
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                image_data = response.content
                image_file = ContentFile(image_data)
                self.file.save(
                    f'{slugify(self.place.title)}_{self.id}.jpg', image_file, save=True)
                print(
                    f'Image successfully loaded and saved to {self.file.path}.')
            except requests.exceptions.RequestException as e:
                print(f'Error downloading image: {e}')
