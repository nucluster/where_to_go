from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import (SortableAdminBase, SortableTabularInline)

from .models import Place, Image


class SortableImageInline(SortableTabularInline):
    fields = ('file', 'get_preview', 'my_order')
    readonly_fields = ('get_preview',)
    ordering = ['my_order']
    model = Image
    extra = 1

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.get_url}" width="50%" height="200px"/>')


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [SortableImageInline, ]


@admin.register(Image)
class SortableImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'url', 'get_preview', 'my_order')
    readonly_fields = ('get_preview',)
    ordering = ['my_order']

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.get_url}" width="200px" height="200px"/>')
