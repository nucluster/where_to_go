from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .models import Image, Place

MAX_WIDTH = 50  # picture preview max width, %
MAX_HEIGHT = 200  # picture height, px


class SortableImageInline(SortableTabularInline):
    fields = ('file', 'get_preview', 'order')
    readonly_fields = ('get_preview',)
    ordering = ('order',)
    model = Image
    extra = 1

    def get_preview(self, image):
        return format_html(
            '<img src={} max-width="{}%" height="{}px"/>',
            image.get_url,
            MAX_WIDTH,
            MAX_HEIGHT
        )


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [SortableImageInline, ]
    search_fields = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        file = cleaned_data.get('file')
        if not url and not file:
            raise forms.ValidationError('Должно быть заполнено поле "Внешний URL" или "Файл"')
        return cleaned_data


@admin.register(Image)
class SortableImageAdmin(admin.ModelAdmin):
    form = ImageForm
    exclude = ('order', 'image_number')
    list_display = ('id', 'file', 'url', 'get_preview')
    readonly_fields = ('get_preview',)
    ordering = ('order',)
    autocomplete_fields = ('place',)

    def get_preview(self, image):
        return format_html(
            '<img src={} max-width="{}%" height="{}px"/>',
            image.get_url,
            MAX_WIDTH,
            MAX_HEIGHT
        )
