import os

from django.db import models
import uuid

from django.conf import settings


def user_directory_path(instance, filename):
    uniqfilename = f"{instance.id}.{filename.split('.')[-1]}"
    return f'place_imgs/{uniqfilename}'


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название места')
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    coordinates = models.JSONField(verbose_name='Географические координаты')
    imgs = models.ManyToManyField('Image', related_name='places',
                                  verbose_name='Фотографии')

    def __str__(self):
        return self.title


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=user_directory_path,
                              verbose_name='Фотография')

    def __str__(self):
        return f'Фото {self.pk}'
