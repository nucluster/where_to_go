from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from .models import Image, Place


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
    inlines = [SortableImageInline, ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


@admin.register(Image)
class SortableImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'url', 'get_preview', 'order')
    readonly_fields = ('get_preview',)
    ordering = ('order',)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.get_url}" width="200px" height="200px"/>')
