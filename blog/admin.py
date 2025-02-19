from django.contrib import admin
from .models import Category, Post, NewsletterSubscriber

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_featured')
    list_filter = ('category', 'created_at', 'is_featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active', 'get_categories')
    list_filter = ('is_active', 'created_at', 'categories')
    search_fields = ('email',)
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Subscribed Categories'

    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = "Activate selected subscribers"

    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
