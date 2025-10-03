from django.contrib import admin
from .models import User, Profile, UserContact
from skills.models import Skill, UserSkill, CV


admin.site.register(UserContact)
# Inline pour UserContact dans UserAdmin
class UserContactInline(admin.TabularInline):
    model = UserContact
    extra = 1
    fields = ['contact_type', 'value', 'label', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

# Inline pour UserSkill dans ProfileAdmin
class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1
    fields = ['skill', 'level', 'years_experience', 'details']
    autocomplete_fields = ['skill']

# Inline pour CV dans ProfileAdmin
class CVInline(admin.TabularInline):
    model = CV
    extra = 1
    readonly_fields = ['uploaded_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'profile__first_name', 'profile__last_name']
    ordering = ['email']
    inlines = [UserContactInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'geographic_zone', 'subscription_status', 'verified_badge', 'availability', 'last_updated']
    list_filter = ['geographic_zone', 'subscription_status', 'verified_badge', 'availability']
    search_fields = ['user__email', 'first_name', 'last_name']
    autocomplete_fields = ['user']
    inlines = [UserSkillInline, CVInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']
    ordering = ['name']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['profile', 'skill', 'level', 'years_experience']
    list_filter = ['level']
    search_fields = ['profile__user__email', 'skill__name']
    autocomplete_fields = ['profile', 'skill']

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ['profile', 'description', 'uploaded_at']
    search_fields = ['profile__user__email', 'description']
    readonly_fields = ['uploaded_at']
