from django.db import models
from pytils.translit import slugify


class Place(models.Model):
    title = models.CharField('Название места', max_length=255, unique=True)
    short_description = models.TextField('Краткое описание', blank=True)
    long_description = models.TextField('Полное описание', blank=True)
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


def user_directory_path(img, filename):
    extension = filename.split('.')[-1]
    filename = f'{slugify(img.place.title)}_{img.image_number}.{extension}'
    return f'places/{filename}'


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE,
        related_name='images', verbose_name='Место'
    )
    file = models.ImageField(
        upload_to=user_directory_path, verbose_name='Файл', blank=True,
        null=True
    )
    url = models.URLField(blank=True, verbose_name='Внешний URL')
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Позиция',
        db_index=True
    )
    image_number = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Порядковый номер фото', default=0)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    def __str__(self):
        return f'{self.image_number} {self.place.title}'

    @property
    def get_url(self):
        if not self.file:
            return self.url
        return self.file.url

    def save(self, *args, **kwargs):
        if not self.image_number:
            last_image = Image.objects.filter(
                place=self.place).order_by('-image_number').first()
            if last_image:
                self.image_number = last_image.image_number + 1
            else:
                self.image_number = 1
        super().save(*args, **kwargs)
