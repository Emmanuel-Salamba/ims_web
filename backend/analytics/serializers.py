# analytics/serializers.py
from rest_framework import serializers
from .models import ActivityLog, AnalyticsData

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'username', 'action', 'model_name', 'object_repr', 'timestamp']
        read_only_fields = fields

class AnalyticsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsData
        fields = ['id', 'content_item', 'date', 'views', 'unique_views', 'downloads', 'shares']