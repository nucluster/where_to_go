import uuid
from django.db import models

from pytils.translit import slugify


def user_directory_path(instance, filename):
    uniq_filename = f"{instance.id}.{filename.split('.')[-1]}"
    return f'place_images/{uniq_filename}'


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название места')
    slug = models.CharField(verbose_name='slug', max_length=255, blank=True,
                            unique=True)
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')
    images = models.ManyToManyField('Image', related_name='places',
                                    verbose_name='Фотографии')

    def __str__(self):
        return self.title

    @property
    def coordinates(self):
        return {'lng': str(self.longitude), 'lat': str(self.latitude)}

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=user_directory_path,
                              verbose_name='Фотография', blank=True)
    extra_url = models.URLField(blank=True, verbose_name='Внешний URL')

    def __str__(self):
        return f'Фото {self.pk}'
