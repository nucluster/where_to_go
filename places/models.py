from django.db import models


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
    image = models.ImageField(upload_to='place_imgs/',
                              verbose_name='Фотография')

    def __str__(self):
        return f'Фото {self.pk}'
