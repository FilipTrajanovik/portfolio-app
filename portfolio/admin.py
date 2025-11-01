from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Profile, Skill, Education, Project,
    Experience, Certificate, ContactMessage, BlogPost
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url')
        }),
        ('Documents', {
            'fields': ('resume_file',)
        }),
    )

    def has_add_permission(self, request):

        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    list_editable = ['proficiency', 'order']
    ordering = ['category', 'order']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current']
    list_editable = ['order']
    date_hierarchy = 'start_date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'status', 'featured', 'order', 'created_at']
    list_filter = ['project_type', 'status', 'featured']
    list_editable = ['featured', 'order', 'status']
    search_fields = ['title', 'description', 'technologies']
    prepopulated_fields = {}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'description', 'image')
        }),
        ('Project Details', {
            'fields': ('project_type', 'status', 'technologies', 'start_date', 'end_date')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Display Options', {
            'fields': ('featured', 'order')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current']
    list_editable = ['order']
    date_hierarchy = 'start_date'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'issue_date', 'expiry_date', 'order']
    list_editable = ['order']
    date_hierarchy = 'issue_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'views', 'created_at']
    list_filter = ['published', 'created_at']
    list_editable = ['published']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'