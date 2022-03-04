from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200)
    placeId = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    description_short = models.CharField(max_length=256, blank=True)
    description_long = models.TextField(blank=True)

    def __str__(self):
        return self.title
