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
    file = models.ImageField(upload_to='place_images/',
                             verbose_name='Файл', blank=True)
    url = models.URLField(blank=True, verbose_name='Внешний URL')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-id']

    def __str__(self):
        return f'{self.pk} {self.place.title}'
