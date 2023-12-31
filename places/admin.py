from django.contrib import admin
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image.places.through
    extra = 1


@admin.register(Place)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'coordinates',)
    inlines = [ImageInline]
    search_fields = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image',)
