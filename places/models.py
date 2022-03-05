from django.db import models


def media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/placeId/<filename>
    return '{0}/{1}'.format(instance.place.placeId, filename)


class Place(models.Model):
    title = models.CharField(max_length=200)
    placeId = models.CharField(max_length=200, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()
    description_short = models.CharField(max_length=256, blank=True)
    description_long = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True, upload_to=media_directory_path)

    def __str__(self):
        return str(self.id) + ' ' + self.place.title
