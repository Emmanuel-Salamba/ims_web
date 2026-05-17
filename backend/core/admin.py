# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import ChurchLeadership, ServiceTime, PrayerRequest

# ============================================
# CUSTOM USER ADMIN - Remove/Hide Important Dates
# ============================================

# Unregister the default User admin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin - Important dates removed
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # Important dates section is REMOVED (commented out)
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Optional customizations
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# ============================================
# YOUR EXISTING CODE BELOW
# ============================================

@admin.register(ChurchLeadership)
class ChurchLeadershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'title', 'order', 'is_active', 'display_photo']
    list_editable = ['order']
    list_filter = ['is_active', 'position']
    search_fields = ['name', 'position', 'title', 'email']
    ordering = ['order', 'name']
    
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return format_html('<span style="color: gray;">No Photo</span>')
    display_photo.short_description = "Photo"

@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_name', 'day', 'start_time', 'end_time', 'is_virtual', 'order', 'is_active']
    list_editable = ['order']
    list_filter = ['day', 'is_virtual', 'is_active']
    search_fields = ['service_name', 'description']
    ordering = ['order', 'day', 'start_time']

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'is_answered', 'is_public']
    list_filter = ['is_answered', 'is_public', 'created_at']
    search_fields = ['name', 'email', 'request']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_answered']
    
    fieldsets = (
        ('Requester Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Prayer Request', {
            'fields': ('request', 'is_public')
        }),
        ('Response', {
            'fields': ('is_answered', 'answer_notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )