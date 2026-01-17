from django.utils.html import format_html
from django.contrib import admin
from .models import Resort
@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'price_per_night',
        'is_active',
        'image_preview'
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" style="border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image"
