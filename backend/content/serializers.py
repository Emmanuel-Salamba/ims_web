# content/serializers.py
from rest_framework import serializers
from .models import ContentItem, Event, Gallery, GalleryImage, Ministry, ContentCategory, ScriptureReading


# ============================================
# CONTENT CATEGORY SERIALIZER
# ============================================

class ContentCategorySerializer(serializers.ModelSerializer):
    """Serializer for Content Categories"""
    class Meta:
        model = ContentCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'parent']


# ============================================
# CONTENT ITEM SERIALIZER
# ============================================

class ContentItemSerializer(serializers.ModelSerializer):
    """Serializer for Content Items (sermons, videos, songs, literature)"""
    thumbnail_url = serializers.SerializerMethodField()
    local_video_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    categories_data = ContentCategorySerializer(source='categories', many=True, read_only=True)
    
    class Meta:
        model = ContentItem
        fields = [
            'id', 'title', 'title_ch', 'description', 'description_ch', 'content_type',
            'youtube_url', 'youtube_video_id', 'thumbnail_url', 'local_video_url',
            'audio_url', 'pdf_url', 'pdf_category', 'author', 'publication_date',
            'duration', 'speaker', 'bible_verses', 'tags', 'is_downloadable',
            'view_count', 'download_count', 'categories_data', 'featured', 'publish_date'
        ]
    
    def get_thumbnail_url(self, obj):
        """Get thumbnail URL from uploaded image or YouTube"""
        if obj.thumbnail:
            return obj.thumbnail.url
        if obj.youtube_video_id:
            return f"https://img.youtube.com/vi/{obj.youtube_video_id}/maxresdefault.jpg"
        return None
    
    def get_local_video_url(self, obj):
        """Get local video file URL if exists"""
        if obj.local_video:
            return obj.local_video.url
        return None
    
    def get_audio_url(self, obj):
        """Get audio file URL if exists"""
        if obj.audio_file:
            return obj.audio_file.url
        return None
    
    def get_pdf_url(self, obj):
        """Get PDF file URL if exists"""
        if obj.pdf_file:
            return obj.pdf_file.url
        return None


# ============================================
# EVENT SERIALIZER
# ============================================

class EventSerializer(serializers.ModelSerializer):
    """Serializer for Events"""
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'title_ch', 'description', 'description_ch',
            'event_date', 'end_date', 'location', 'location_link',
            'is_virtual', 'virtual_link', 'featured_image', 'is_featured', 
            'is_upcoming', 'is_active', 'created_at'
        ]


# ============================================
# GALLERY IMAGE SERIALIZER
# ============================================

class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for individual Gallery Images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = ['id', 'image_url', 'caption', 'caption_ch', 'order']
    
    def get_image_url(self, obj):
        """Get the full URL of the image"""
        if obj.image:
            return obj.image.url
        return None


# ============================================
# GALLERY SERIALIZER
# ============================================

class GallerySerializer(serializers.ModelSerializer):
    """Serializer for Photo Galleries with Chichewa support"""
    images = GalleryImageSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallery
        fields = [
            'id', 'title', 'title_ch', 'description', 'description_ch',
            'cover_image_url', 'event_date', 'images', 'is_active', 'created_at'
        ]
    
    def get_cover_image_url(self, obj):
        """Get the full URL of the cover image"""
        if obj.cover_image:
            return obj.cover_image.url
        return None


# ============================================
# MINISTRY SERIALIZER - WITH NULLABLE FIELDS
# ============================================

class MinistrySerializer(serializers.ModelSerializer):
    """Serializer for Church Ministries with Chichewa support and nullable fields"""
    image_url = serializers.SerializerMethodField()
    
    # Add helper fields for frontend to check if fields are present
    has_leader = serializers.SerializerMethodField()
    has_meeting = serializers.SerializerMethodField()
    meeting_time_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'name_ch', 'description', 'description_ch',
            'leader', 'leader_contact', 'meeting_day', 'meeting_time',
            'icon', 'image_url', 'order', 'is_active',
            'has_leader', 'has_meeting', 'meeting_time_display'
        ]
    
    def get_image_url(self, obj):
        """Get the full URL of the ministry image"""
        if obj.image:
            return obj.image.url
        return None
    
    def get_has_leader(self, obj):
        """Check if ministry has leader information"""
        return bool(obj.leader and obj.leader.strip())
    
    def get_has_meeting(self, obj):
        """Check if ministry has meeting information"""
        return bool(obj.meeting_day and obj.meeting_day.strip())
    
    def get_meeting_time_display(self, obj):
        """Format meeting time for display or return None"""
        if obj.meeting_time:
            return obj.meeting_time.strftime('%I:%M %p')
        return None


# ============================================
# MINISTRY DETAIL SERIALIZER (More detailed)
# ============================================

class MinistryDetailSerializer(MinistrySerializer):
    """Detailed Ministry Serializer with additional info"""
    full_leader_info = serializers.SerializerMethodField()
    full_meeting_info = serializers.SerializerMethodField()
    
    class Meta(MinistrySerializer.Meta):
        fields = MinistrySerializer.Meta.fields + ['full_leader_info', 'full_meeting_info']
    
    def get_full_leader_info(self, obj):
        """Return complete leader information or None"""
        if obj.leader:
            return {
                'name': obj.leader,
                'contact': obj.leader_contact if obj.leader_contact else None
            }
        return None
    
    def get_full_meeting_info(self, obj):
        """Return complete meeting information or None"""
        if obj.meeting_day:
            return {
                'day': obj.meeting_day,
                'time': obj.meeting_time.strftime('%I:%M %p') if obj.meeting_time else None
            }
        return None


# ============================================
# SCRIPTURE READING SERIALIZER - WITH CHICHEWA FIELDS
# ============================================

class ScriptureReadingSerializer(serializers.ModelSerializer):
    """Serializer for Scripture Readings with Chichewa support"""
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    
    # Helper fields for frontend
    has_chichewa = serializers.SerializerMethodField()
    has_title = serializers.SerializerMethodField()
    display_title = serializers.SerializerMethodField()
    
    class Meta:
        model = ScriptureReading
        fields = [
            'id', 'date',
            'title', 'bible_verse', 'spirit_of_prophecy',
            'title_ch', 'bible_verse_ch', 'spirit_of_prophecy_ch',
            'has_chichewa', 'has_title', 'display_title',
            'created_at', 'updated_at', 'created_by_name', 'updated_by_name'
        ]
    
    def get_created_by_name(self, obj):
        """Get the name of the user who created this reading"""
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None
    
    def get_updated_by_name(self, obj):
        """Get the name of the user who last updated this reading"""
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return None
    
    def get_has_chichewa(self, obj):
        """Check if Chichewa translation exists"""
        return bool(obj.bible_verse_ch and obj.bible_verse_ch.strip())
    
    def get_has_title(self, obj):
        """Check if title exists (English or Chichewa)"""
        return bool((obj.title and obj.title.strip()) or (obj.title_ch and obj.title_ch.strip()))
    
    def get_display_title(self, obj):
        """Get the best available title (English preferred, fallback to Chichewa)"""
        if obj.title and obj.title.strip():
            return obj.title
        elif obj.title_ch and obj.title_ch.strip():
            return obj.title_ch
        return f"Reading for {obj.date}"


# ============================================
# DETAILED GALLERY SERIALIZER (with full image details)
# ============================================

class GalleryDetailSerializer(GallerySerializer):
    """Detailed Gallery Serializer with additional metadata"""
    image_count = serializers.SerializerMethodField()
    cover_image_thumbnail = serializers.SerializerMethodField()
    
    class Meta(GallerySerializer.Meta):
        fields = GallerySerializer.Meta.fields + ['image_count', 'cover_image_thumbnail']
    
    def get_image_count(self, obj):
        """Get the total number of images in the gallery"""
        return obj.images.count()
    
    def get_cover_image_thumbnail(self, obj):
        """Get a thumbnail version of the cover image"""
        if obj.cover_image:
            return obj.cover_image.url
        return None


# ============================================
# SIMPLE MINISTRY SERIALIZER (for dropdowns)
# ============================================

class SimpleMinistrySerializer(serializers.ModelSerializer):
    """Simple serializer for ministry dropdown menus"""
    class Meta:
        model = Ministry
        fields = ['id', 'name', 'is_active']


# ============================================
# MINISTRY LIST SERIALIZER (Optimized for listing)
# ============================================

class MinistryListSerializer(serializers.ModelSerializer):
    """Optimized serializer for ministry listing pages"""
    image_url = serializers.SerializerMethodField()
    has_meeting = serializers.SerializerMethodField()
    
    class Meta:
        model = Ministry
        fields = ['id', 'name', 'name_ch', 'description', 'description_ch', 
                  'image_url', 'order', 'has_meeting', 'is_active']
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def get_has_meeting(self, obj):
        return bool(obj.meeting_day and obj.meeting_day.strip())


# ============================================
# SIMPLE SCRIPTURE READING SERIALIZER
# ============================================

class SimpleScriptureReadingSerializer(serializers.ModelSerializer):
    """Simple serializer for listing pages"""
    display_title = serializers.SerializerMethodField()
    
    class Meta:
        model = ScriptureReading
        fields = ['id', 'date', 'display_title']
    
    def get_display_title(self, obj):
        if obj.title and obj.title.strip():
            return obj.title
        elif obj.title_ch and obj.title_ch.strip():
            return obj.title_ch
        return f"Reading for {obj.date}"