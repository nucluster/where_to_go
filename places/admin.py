from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableAdminMixin, SortableAdminBase, SortableTabularInline

from .models import Place, Image


class ImageInline(SortableTabularInline):
    fields = ('file', 'get_preview', 'my_order')
    readonly_fields = ('get_preview',)
    ordering = ['my_order']
    model = Image
    extra = 1

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" width="200px" height="200px"/>')


@admin.register(Place)
class SortablePlaceAdmin(admin.ModelAdmin, SortableAdminMixin):
    inlines = [ImageInline, ]


@admin.register(Image)
class SortableImageAdmin(admin.ModelAdmin, SortableAdminMixin):
    ordering = ['my_order']
    list_display = ('file', 'url', 'my_order')
    readonly_fields = ('get_preview',)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" width="200px" height="200px"/>')
