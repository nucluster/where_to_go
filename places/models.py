import uuid
from django.db import models


def user_directory_path(instance, filename):
    uniq_filename = f"{instance.id}.{filename.split('.')[-1]}"
    return f'place_images/{uniq_filename}'


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to=user_directory_path,
                             verbose_name='Фотография', blank=True)
    url = models.URLField(blank=True, verbose_name='Внешний URL')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-id']

    def __str__(self):
        return f'Фото {self.id}'
