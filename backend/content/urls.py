# content/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'content', views.ContentItemViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'galleries', views.GalleryViewSet)
router.register(r'ministries', views.MinistryViewSet)
router.register(r'categories', views.ContentCategoryViewSet)
router.register(r'scripture-readings', views.ScriptureReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('gallery/<int:pk>/images/', views.GalleryImageViewSet.as_view({'get': 'list'}), name='gallery-images'),
]