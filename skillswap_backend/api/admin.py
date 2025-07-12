from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, SwapRequest, Feedback


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'name', 'location', 'is_public', 'is_active']
    list_filter = ['is_public', 'is_active', 'date_joined']
    search_fields = ['email', 'name', 'location']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'location', 'profile_photo', 'availability', 'is_public')}),
        ('Skills', {'fields': ('skills_offered', 'skills_wanted')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'offered_skill', 'requested_skill', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['sender__name', 'receiver__name', 'offered_skill__name', 'requested_skill__name']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'rating', 'swap_request', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['from_user__name', 'to_user__name', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
