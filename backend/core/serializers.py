# core/serializers.py
from rest_framework import serializers
from .models import ChurchLeadership, ServiceTime, PrayerRequest

class ChurchLeadershipSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ChurchLeadership
        fields = ['id', 'name', 'title', 'position', 'bio', 'email', 'phone', 'photo_url', 'order']
    
    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

class ServiceTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTime
        fields = ['id', 'day', 'service_name', 'start_time', 'end_time', 'description', 'is_virtual', 'virtual_link']

class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = ['id', 'name', 'email', 'phone', 'request', 'is_public']
        read_only_fields = ['created_at', 'is_answered']