from django.db import models
from django.core.cache import cache

class SiteSettings(models.Model):
    # Site Identity
    site_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site/logo/')
    favicon = models.ImageField(upload_to='site/favicon/')
    preloader = models.ImageField(upload_to='site/preloader/', blank=True, help_text="Upload preloader image")
    
    # Hero Section
    hero_video = models.FileField(upload_to='site/hero/', blank=True)
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    
    # About Section
    about_image = models.ImageField(upload_to='site/about/')
    about_title = models.CharField(max_length=200, null=True)  # Added field
    about_content = models.TextField(null=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    phone2 = models.CharField(max_length=20, blank=True, help_text="Secondary phone number")
    google_map_embed = models.TextField(blank=True)
    
    # Social Media Links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    
    # SEO Settings
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Footer
    footer_text = models.TextField()
    copyright_text = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache when settings are updated
        cache.delete('site_settings')
