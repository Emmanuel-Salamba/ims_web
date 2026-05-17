# analytics/admin.py
from django.contrib import admin
from .models import ActivityLog, AnalyticsData

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'action', 'model_name', 'object_repr', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['username', 'object_repr', 'model_name']
    readonly_fields = [f.name for f in ActivityLog._meta.fields]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion of old logs

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'date', 'views', 'downloads']
    list_filter = ['content_type', 'date']
    search_fields = ['content_type', 'object_id']
    readonly_fields = ['date']