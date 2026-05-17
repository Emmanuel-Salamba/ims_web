# payments/admin.py
from django.contrib import admin
from .models import Donation, PaymentSetting

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor_name', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'is_anonymous', 'is_recurring', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'donor_phone', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_method', 'transaction_id', 'status', 'notes')
        }),
        ('Recurring Donation', {
            'fields': ('is_recurring', 'recurring_frequency'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PaymentSetting)
class PaymentSettingAdmin(admin.ModelAdmin):
    list_display = ['payment_method', 'is_enabled', 'merchant_id']
    list_editable = ['is_enabled']
    fieldsets = (
        ('Basic Settings', {
            'fields': ('payment_method', 'is_enabled', 'instructions')
        }),
        ('API Configuration', {
            'fields': ('api_key', 'api_secret', 'merchant_id', 'callback_url'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow editing existing payment methods
        if PaymentSetting.objects.count() >= 4:
            return False
        return True