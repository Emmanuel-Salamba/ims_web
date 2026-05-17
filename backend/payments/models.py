from django.db import models

class Donation(models.Model):
    """Donation/payment model"""
    PAYMENT_METHODS = [
        ('airtel', 'Airtel Money'),
        ('tnm', 'TNM Mpamba'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=200, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=20, blank=True, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Donation of {self.amount} by {self.donor_name}"
    
    class Meta:
        ordering = ['-created_at']

class PaymentSetting(models.Model):
    """Payment gateway settings"""
    payment_method = models.CharField(max_length=20, unique=True, choices=Donation.PAYMENT_METHODS)
    is_enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    merchant_id = models.CharField(max_length=100, blank=True)
    callback_url = models.URLField(blank=True)
    instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.payment_method} Settings"