# # payments/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'donations', views.DonationViewSet)
# router.register(r'settings', views.PaymentSettingViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     path('webhook/airtel/', views.airtel_webhook, name='airtel-webhook'),
#     path('webhook/tnm/', views.tnm_webhook, name='tnm-webhook'),
# ]


from django.urls import path

urlpatterns = [
    # Views will be added later
]