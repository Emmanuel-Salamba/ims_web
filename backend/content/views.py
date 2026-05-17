# content/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContentItem, Event, Gallery, GalleryImage, Ministry, ContentCategory, ScriptureReading
from .serializers import (
    ContentItemSerializer, EventSerializer, GallerySerializer, GalleryImageSerializer,
    MinistrySerializer, ContentCategorySerializer, ScriptureReadingSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response

class ContentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ContentCategory.objects.all()
    serializer_class = ContentCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ContentItemViewSet(viewsets.ModelViewSet):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['content_type', 'featured', 'pdf_category', 'is_active']
    search_fields = ['title', 'description', 'speaker', 'author', 'tags']
    ordering_fields = ['publish_date', 'view_count', 'download_count', 'created_at']
    ordering = ['-publish_date']
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        content = self.get_object()
        content.view_count += 1
        content.save()
        return Response({'status': 'view counted', 'views': content.view_count})
    
    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        content = self.get_object()
        content.download_count += 1
        content.save()
        return Response({'status': 'download counted', 'downloads': content.download_count})

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_virtual', 'is_featured']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['event_date']
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        from django.utils import timezone
        upcoming_events = self.get_queryset().filter(event_date__gte=timezone.now(), is_active=True)
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['-event_date']

class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GalleryImageSerializer
    
    def get_queryset(self):
        gallery_id = self.kwargs.get('pk')
        return GalleryImage.objects.filter(gallery_id=gallery_id)

class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.filter(is_active=True)
    serializer_class = MinistrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'leader']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']

class ScriptureReadingViewSet(viewsets.ModelViewSet):
    queryset = ScriptureReading.objects.all()
    serializer_class = ScriptureReadingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date']
    search_fields = ['title', 'bible_verse', 'spirit_of_prophecy']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']