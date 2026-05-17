# core/views.py
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({"status": "healthy", "message": "IMS Malawi Union API is running"})

@csrf_exempt
def custom_logout(request):
    """Custom logout view that handles GET requests"""
    logout(request)
    return redirect('/admin/login/')