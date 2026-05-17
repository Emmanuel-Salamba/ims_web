from django.db import models

class Comment(models.Model):
    """Comments and questions model"""
    content_type = models.CharField(max_length=100, help_text="Model name like 'ContentItem'")
    object_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    comment_text = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_question = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"Comment by {self.user_name}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['created_at']),
        ]