from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class ChurchLeadership(BaseModel):
    """Church leadership model"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='leadership/', null=True, blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} {self.name}"
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Church Leadership"

class ServiceTime(BaseModel):
    """Church service times"""
    day = models.CharField(max_length=50)
    service_name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.service_name} - {self.day}"
    
    class Meta:
        ordering = ['order', 'day', 'start_time']

class PrayerRequest(BaseModel):
    """Prayer requests from congregation"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    request = models.TextField()
    is_public = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    answer_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Prayer request from {self.name}"
    
    class Meta:
        ordering = ['-created_at']