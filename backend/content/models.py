# content/models.py
from django.db import models
from django.core.validators import FileExtensionValidator
from core.models import BaseModel


class ContentCategory(models.Model):
    """Categories for content organization"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Content Categories"
        ordering = ['name']


class ContentItem(BaseModel):
    """Main content model for sermons, videos, songs, literature"""
    CONTENT_TYPES = [
        ('sermon', 'Sermon'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('song', 'Song'),
        ('literature', 'Literature'),
    ]
    
    PDF_CATEGORIES = [
        ('sabbath_school', 'Sabbath School Lessons'),
        ('week_of_prayer', 'Week of Prayer Readings'),
        ('marriage', 'Marriage Readings'),
        ('children', 'Children\'s Ministry'),
        ('youth', 'Youth Ministry'),
        ('general', 'General Literature'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    title_ch = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    description_ch = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    
    # Media URLs and Files
    youtube_url = models.URLField(blank=True, null=True)
    local_video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['mp4', 'avi', 'mov', 'mkv'])]
    )
    audio_file = models.FileField(
        upload_to='audio/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['mp3', 'wav', 'ogg', 'm4a'])]
    )
    pdf_file = models.FileField(
        upload_to='pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])]
    )
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    # Literature specific fields
    pdf_category = models.CharField(max_length=50, choices=PDF_CATEGORIES, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    
    # Additional metadata
    duration = models.CharField(max_length=50, blank=True)
    speaker = models.CharField(max_length=200, blank=True)
    bible_verses = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=500, blank=True)
    
    # Download settings
    is_downloadable = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # Categories and relationships
    categories = models.ManyToManyField(ContentCategory, blank=True)
    featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def youtube_video_id(self):
        """Extract YouTube video ID from URL"""
        if self.youtube_url and 'youtu.be' in self.youtube_url:
            return self.youtube_url.split('/')[-1]
        elif self.youtube_url and 'watch?v=' in self.youtube_url:
            return self.youtube_url.split('v=')[1].split('&')[0]
        return None
    
    class Meta:
        ordering = ['-publish_date', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'publish_date']),
            models.Index(fields=['pdf_category']),
        ]


class Event(BaseModel):
    """Events and announcements model"""
    title = models.CharField(max_length=200)
    title_ch = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    description_ch = models.TextField(blank=True)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=300)
    location_link = models.URLField(blank=True)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True)
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        """Check if event is in the future"""
        from django.utils import timezone
        return self.event_date > timezone.now()
    
    class Meta:
        ordering = ['event_date']


class Gallery(BaseModel):
    """Photo gallery model with Chichewa support"""
    title = models.CharField(max_length=200)
    title_ch = models.CharField(max_length=200, blank=True, help_text="Chichewa translation of title")
    description = models.TextField(blank=True)
    description_ch = models.TextField(blank=True, help_text="Chichewa translation of description")
    cover_image = models.ImageField(upload_to='gallery/covers/')
    event_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-event_date', '-created_at']


class GalleryImage(models.Model):
    """Individual images in gallery"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/images/')
    caption = models.CharField(max_length=200, blank=True)
    caption_ch = models.CharField(max_length=200, blank=True, help_text="Chichewa translation of caption")
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.gallery.title} - Image {self.order}"
    
    class Meta:
        ordering = ['order']


class Ministry(BaseModel):
    """Church ministries model - Leadership and Meeting Details are NULLABLE"""
    name = models.CharField(max_length=100)
    name_ch = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    description_ch = models.TextField(blank=True)
    
    # LEADERSHIP FIELDS - NULLABLE (can be empty)
    leader = models.CharField(max_length=200, blank=True, null=True, help_text="Leave blank if not applicable")
    leader_contact = models.CharField(max_length=100, blank=True, null=True, help_text="Leave blank if not applicable")
    
    # MEETING DETAILS FIELDS - NULLABLE (can be empty)
    meeting_day = models.CharField(max_length=50, blank=True, null=True, help_text="Leave blank if not applicable (e.g., for online-only ministries)")
    meeting_time = models.TimeField(blank=True, null=True, help_text="Leave blank if not applicable")
    
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='ministries/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Ministries"


class ScriptureReading(BaseModel):
    """Scripture readings with Bible and Spirit of Prophecy - WITH CHICHEWA SUPPORT"""
    date = models.DateField(unique=True)
    
    # English fields
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for the reading (English)")
    bible_verse = models.TextField(help_text="Full Bible verse text (English)")
    spirit_of_prophecy = models.TextField(help_text="Spirit of Prophecy/EGW text (English)")
    
    # Chichewa fields
    title_ch = models.CharField(max_length=200, blank=True, null=True, help_text="Optional title for the reading (Chichewa)")
    bible_verse_ch = models.TextField(blank=True, null=True, help_text="Full Bible verse text (Chichewa)")
    spirit_of_prophecy_ch = models.TextField(blank=True, null=True, help_text="Spirit of Prophecy/EGW text (Chichewa)")
    
    def __str__(self):
        if self.title:
            return f"{self.title} - {self.date}"
        return f"Scripture Reading for {self.date}"
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Scripture Reading"
        verbose_name_plural = "Scripture Readings"