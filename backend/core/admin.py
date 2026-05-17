# core/admin.py
from django.contrib import admin
from .models import BaseModel

# All admin registrations for ChurchLeadership, PrayerRequest, and ServiceTime have been removed
# No models remain to register in core app

# Keep this empty or add a message
admin.site.site_header = "IMS Malawi Union Administration"
admin.site.site_title = "IMS Malawi Union Admin"
admin.site.index_title = "Welcome to IMS Malawi Union Admin Panel"