from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resort', 'status', 'check_in', 'check_out')
    list_filter = ('status',)
