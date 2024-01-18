import requests
from django.core.files.base import ContentFile
from django.db import models
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
    file = models.ImageField(
        upload_to='places/', verbose_name='Файл', blank=True)
    url = models.URLField(blank=True, verbose_name='Внешний URL')
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Позиция'
    )
    image_number = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Порядковый номер фото', default=1)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    @property
    def get_url(self):
        if not self.file:
            return self.url
        return self.file.url

    def __str__(self):
        return f'{self.image_number} {self.place.title}'

    def save(self, *args, **kwargs):
        if not self.image_number:
            last_image = Image.objects.filter(
                place=self.place).order_by('-image_number').first()
            if last_image:
                self.image_number = last_image.image_number + 1
        super().save(*args, **kwargs)

    def download_image(self):
        if self.url and not self.file:
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                image_data = response.content
                image_file = ContentFile(image_data)
                self.file.save(
                    f'{slugify(self.place.title)}_{self.image_number}.jpg',
                    image_file, save=True)
                print(
                    f'Image successfully loaded and saved to {self.file.path}.')
            except requests.exceptions.RequestException as e:
                print(f'Error downloading image: {e}')
