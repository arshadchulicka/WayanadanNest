from django.contrib import admin
from .models import CompanyInfo   # change model name as needed

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'email')
from django.contrib import admin
from .models import Carousel

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'discount_percentage',
        'is_active',
        'created_at'
    )
    list_editable = ('is_active',)
    search_fields = ('title',)
