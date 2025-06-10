from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = (
        'bio', 'birth_date', 'location', 'phone_number', 'website',
        'profile_image', 'preferred_language',
        ('linkedin_url', 'github_url', 'twitter_url'),
        ('email_notifications', 'course_updates', 'marketing_emails'),
    )

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'preferred_language', 'created_at')
    list_filter = ('preferred_language', 'email_notifications', 'course_updates', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'bio', 'profile_image')
        }),
        ('Personal Details', {
            'fields': ('birth_date', 'location', 'phone_number', 'website', 'preferred_language')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'course_updates', 'marketing_emails')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Unregister the original User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
