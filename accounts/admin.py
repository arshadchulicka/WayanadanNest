from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'city',
        'state',
        'is_email_verified',
        'is_admin_approved',
    )

    list_editable = ('is_admin_approved',)
    list_filter = ('is_email_verified', 'is_admin_approved', 'state')
    search_fields = ('user__username', 'phone', 'city')

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'phone', 'profile_image')
        }),
        ('Address Details', {
            'fields': ('address', 'city', 'state')
        }),
        ('Verification Status', {
            'fields': ('is_email_verified', 'is_admin_approved')
        }),
    )
