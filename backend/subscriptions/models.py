from django.db import models

class Subscriber(models.Model):
    """Email subscribers model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    receive_sermons = models.BooleanField(default=True)
    receive_events = models.BooleanField(default=True)
    receive_newsletters = models.BooleanField(default=True)
    verification_token = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']

class NotificationLog(models.Model):
    """Log of all email notifications sent"""
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300)
    content_type = models.CharField(max_length=50)
    content_id = models.PositiveIntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')
    
    def __str__(self):
        return f"Notification to {self.subscriber.email}"