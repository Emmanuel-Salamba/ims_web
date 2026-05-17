# ims_malawi_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView

@csrf_exempt
def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')

urlpatterns = [
    # Favicon
    path('favicon.ico', RedirectView.as_view(url='/media/logos/ims-icon.png', permanent=True)),
    
    # i18n for language switching
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Redirect for accounts/profile (fixes login redirect)
    path('accounts/profile/', RedirectView.as_view(url='/admin/', permanent=False)),
    
    # Custom logout
    path('admin/logout/', admin_logout, name='admin_logout'),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/core/', include('core.urls')),
    path('api/content/', include('content.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/analytics/', include('analytics.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)