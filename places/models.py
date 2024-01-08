# from django.conf import settings
from django.db import models


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
