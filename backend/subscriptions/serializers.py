# subscriptions/serializers.py
from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'name', 'receive_sermons', 'receive_events', 'receive_newsletters']