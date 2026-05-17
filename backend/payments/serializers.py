# payments/serializers.py
from rest_framework import serializers
from .models import Donation, PaymentSetting

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'donor_name', 'donor_email', 'donor_phone', 'amount', 
                  'payment_method', 'status', 'is_anonymous', 'is_recurring', 'recurring_frequency']
        read_only_fields = ['status', 'transaction_id']

class PaymentSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSetting
        fields = ['payment_method', 'is_enabled', 'instructions']