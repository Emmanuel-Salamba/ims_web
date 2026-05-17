# subscriptions/admin.py
from django.contrib import admin
from django.http import HttpResponse
from .models import Subscriber, NotificationLog
import csv

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'subscribed_at', 'is_active', 'is_verified']
    list_filter = ['is_active', 'is_verified', 'receive_sermons', 'receive_events', 'receive_newsletters']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'verification_token']
    actions = ['export_as_csv', 'activate_subscribers', 'deactivate_subscribers']
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Subscribed Date', 'Active', 'Verified', 'Sermons', 'Events', 'Newsletters'])
        for subscriber in queryset:
            writer.writerow([
                subscriber.email, 
                subscriber.name, 
                subscriber.subscribed_at,
                subscriber.is_active,
                subscriber.is_verified,
                subscriber.receive_sermons,
                subscriber.receive_events,
                subscriber.receive_newsletters
            ])
        return response
    export_as_csv.short_description = "Export Selected Subscribers to CSV"
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = "Deactivate selected subscribers"

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'subscriber', 'subject', 'content_type', 'sent_at', 'status']
    list_filter = ['status', 'content_type', 'sent_at']
    search_fields = ['subscriber__email', 'subject']
    readonly_fields = [f.name for f in NotificationLog._meta.fields]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False