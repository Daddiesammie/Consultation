from django.contrib import admin
from .models import Portfolio, Service, Testimonial, Contact, TeamMember, Award

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'rating', 'created_at')
    search_fields = ('client_name', 'company', 'content')
    list_filter = ('rating', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'completion_date', 'is_featured')
    search_fields = ('title', 'description', 'client')
    list_filter = ('completion_date', 'is_featured')
    date_hierarchy = 'completion_date'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_key_member', 'order')
    search_fields = ('name', 'position', 'bio')
    list_filter = ('is_key_member', 'created_at')
    list_editable = ('order', 'is_key_member')
    date_hierarchy = 'created_at'

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date_received', 'is_featured')
    search_fields = ('title', 'organization', 'description')
    list_filter = ('is_featured', 'date_received')
    date_hierarchy = 'date_received'
