# content/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ContentItem, Event, Gallery, GalleryImage, Ministry, ContentCategory, ScriptureReading

# ============================================
# INLINE CLASSES
# ============================================

class GalleryImageInline(admin.TabularInline):
    """Inline form for gallery images"""
    model = GalleryImage
    extra = 3
    fields = ['image', 'caption', 'caption_ch', 'order']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'caption_ch':
            kwargs['help_text'] = 'Chichewa translation of the caption (leave blank if not available)'
        return super().formfield_for_dbfield(db_field, **kwargs)


# ============================================
# MODEL ADMIN CLASSES
# ============================================

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Content Categories"""
    list_display = ['name', 'slug', 'parent']
    list_display_links = ['name']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Hierarchy', {
            'fields': ('parent',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    """Admin configuration for Content Items (sermons, videos, songs, literature)"""
    list_display = ['title', 'content_type', 'speaker', 'publish_date', 'view_count', 'download_count', 'featured']
    list_display_links = ['title']
    list_filter = ['content_type', 'featured', 'pdf_category', 'is_active', 'publish_date']
    search_fields = ['title', 'description', 'speaker', 'author', 'tags']
    readonly_fields = ['view_count', 'download_count', 'created_at', 'updated_at', 'publish_date']
    list_editable = ['featured']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_ch', 'description', 'description_ch', 'content_type')
        }),
        ('Media Content', {
            'fields': ('youtube_url', 'local_video', 'audio_file', 'pdf_file', 'thumbnail')
        }),
        ('Literature Details', {
            'fields': ('pdf_category', 'author', 'publication_date'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('duration', 'speaker', 'bible_verses', 'tags', 'categories', 'featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('view_count', 'download_count', 'is_downloadable'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin configuration for Events"""
    list_display = ['title', 'event_date', 'end_date', 'location', 'is_virtual', 'is_featured']
    list_display_links = ['title']
    list_filter = ['is_virtual', 'is_featured', 'event_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'title_ch', 'description', 'description_ch')
        }),
        ('Date & Location', {
            'fields': ('event_date', 'end_date', 'location', 'location_link')
        }),
        ('Virtual Options', {
            'fields': ('is_virtual', 'virtual_link'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('featured_image', 'is_featured', 'is_active')
        }),
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Admin configuration for Photo Galleries with Chichewa support"""
    list_display = ['title', 'event_date', 'created_at', 'image_count']
    list_display_links = ['title']
    list_filter = ['event_date', 'created_at', 'is_active']
    search_fields = ['title', 'description', 'title_ch', 'description_ch']
    inlines = [GalleryImageInline]
    
    fieldsets = (
        ('English Version', {
            'fields': ('title', 'description')
        }),
        ('Chichewa Version', {
            'fields': ('title_ch', 'description_ch'),
            'classes': ('collapse',),
            'description': 'Chichewa translations (leave blank if not available)'
        }),
        ('Gallery Settings', {
            'fields': ('cover_image', 'event_date', 'is_active')
        }),
    )
    
    def image_count(self, obj):
        """Display the number of images in the gallery"""
        count = obj.images.count()
        return format_html('<span style="color: #2F5D50; font-weight: bold;">{} image{}</span>', 
                          count, 's' if count != 1 else '')
    image_count.short_description = "Number of Images"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    """Admin configuration for Church Ministries"""
    list_display = ['name', 'leader', 'meeting_day', 'meeting_time', 'order', 'is_active']
    list_display_links = ['name']
    list_editable = ['order']
    list_filter = ['is_active', 'meeting_day']
    search_fields = ['name', 'description', 'leader']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('English Version', {
            'fields': ('name', 'description')
        }),
        ('Chichewa Version', {
            'fields': ('name_ch', 'description_ch'),
            'classes': ('collapse',),
            'description': 'Chichewa translations (leave blank if not available)'
        }),
        ('Leadership (Optional)', {
            'fields': ('leader', 'leader_contact'),
            'classes': ('collapse',),
            'description': 'These fields are optional. Leave blank if not applicable.'
        }),
        ('Meeting Details (Optional)', {
            'fields': ('meeting_day', 'meeting_time'),
            'classes': ('collapse',),
            'description': 'These fields are optional. Leave blank if the ministry does not have regular meetings.'
        }),
        ('Display Settings', {
            'fields': ('icon', 'image', 'order', 'is_active')
        }),
    )


@admin.register(ScriptureReading)
class ScriptureReadingAdmin(admin.ModelAdmin):
    """Admin configuration for Scripture Readings with Chichewa support"""
    list_display = ['date', 'title', 'get_bible_preview', 'created_at']
    list_display_links = ['date']
    list_filter = ['date', 'created_at']
    search_fields = ['title', 'title_ch', 'bible_verse', 'bible_verse_ch', 'spirit_of_prophecy', 'spirit_of_prophecy_ch']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Date Information', {
            'fields': ('date',)
        }),
        ('English Version', {
            'fields': ('title', 'bible_verse', 'spirit_of_prophecy'),
            'description': 'English version of the scripture reading'
        }),
        ('Chichewa Version', {
            'fields': ('title_ch', 'bible_verse_ch', 'spirit_of_prophecy_ch'),
            'classes': ('collapse',),
            'description': 'Chichewa translation (leave blank if not available)'
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_bible_preview(self, obj):
        """Preview of bible verse (English)"""
        if obj.bible_verse and len(obj.bible_verse) > 100:
            return obj.bible_verse[:100] + '...'
        return obj.bible_verse or 'No verse entered'
    get_bible_preview.short_description = "Bible Verse Preview (EN)"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)