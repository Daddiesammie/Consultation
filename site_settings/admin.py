from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon')
        }),
        ('Hero Section', {
            'fields': ('hero_video', 'hero_title', 'hero_subtitle')
        }),
        ('About Section', {
            'fields': ('about_image', 'about_title', 'about_content',)  # Note the comma to make it a tuple
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'google_map_embed')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'google_analytics_id')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
    )
