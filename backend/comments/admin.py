# comments/admin.py
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'content_type', 'object_id', 'created_at', 'is_approved', 'is_question']
    list_filter = ['is_approved', 'is_question', 'created_at']
    search_fields = ['user_name', 'user_email', 'comment_text']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'content_type', 'object_id', 'ip_address', 'user_agent']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"