from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    """Activity log for tracking system actions"""
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('archive', 'Archive'),
        ('restore', 'Restore'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('download', 'Download'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, db_index=True)
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __str__(self):
        return f"{self.username} - {self.action} - {self.object_repr}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'action']),
            models.Index(fields=['username']),
        ]

class AnalyticsData(models.Model):
    """Analytics for content performance"""
    content_type = models.CharField(max_length=100, help_text="Model name like 'ContentItem'")
    object_id = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.content_type}_{self.object_id} - {self.date}"
    
    class Meta:
        unique_together = ['content_type', 'object_id', 'date']
        ordering = ['-date']
        verbose_name_plural = "Analytics Data"