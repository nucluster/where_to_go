from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from adminsortable2.admin import (SortableAdminBase, SortableTabularInline)
from tinymce.widgets import TinyMCE

from .models import Place, Image


class SortableImageInline(SortableTabularInline):
    fields = ('file', 'get_preview', 'order')
    readonly_fields = ('get_preview',)
    ordering = ('order',)
    model = Image
    extra = 1

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.get_url}" width="50%" height="200px"/>')


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    exclude = ('order', 'image_number')
    inlines = [SortableImageInline, ]
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
            raise forms.ValidationError("Должно быть заполнено поле 'Внешний URL' или 'Файл'")
        return cleaned_data


@admin.register(Image)
class SortableImageAdmin(admin.ModelAdmin):
    form = ImageForm
    list_display = ('file', 'url', 'get_preview', 'order')
    readonly_fields = ('get_preview',)
    ordering = ('order',)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.get_url}" width="200px" height="200px"/>')
