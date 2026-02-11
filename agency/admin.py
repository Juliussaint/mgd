from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, Service, ServiceFeature, TeamMember, ContactInquiry, ProjectCategory, ProjectImage

# --- 1. PROJECT ADMIN ---

# Inline untuk Galeri Gambar
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ('order', 'image')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'client_name', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'client_name', 'technologies')
    ordering = ('-created_at',)
    
    # Sambungkan Inline Galeri
    inlines = [ProjectImageInline] 
    
    fieldsets = (
        ('Project Information', {'fields': ('title', 'slug', 'client_name', 'category')}),
        ('Content', {'fields': ('description', 'technologies', 'project_url', 'featured')}),
        ('Thumbnail', {'fields': ('thumbnail',)}),
    )

    # --- FIX: Menambahkan Method Thumbnail Preview ---
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="60" height="60" style="object-fit:cover; border-radius: 4px;">')
        return "No Image"
    thumbnail_preview.short_description = 'Image'


# --- 2. SERVICE ADMIN ---

# Inline untuk Fitur Service
class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3
    fields = ('order', 'title', 'description')
    ordering = ('order',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [ServiceFeatureInline]
    
    # --- FIX: Slug otomatis dari judul ---
    prepopulated_fields = {'slug': ('title',)}


# --- 3. TEAM MEMBER ADMIN ---
@admin.register(TeamMember)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'role')
    search_fields = ('name', 'role')
    
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'role', 'bio')}),
        ('Photo', {'fields': ('photo',)}),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit:cover; border-radius: 50%;">')
        return "No Photo"
    photo_preview.short_description = 'Avatar'


# --- 4. CATEGORY ADMIN ---
@admin.register(ProjectCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# --- 5. CONTACT INQUIRY ADMIN ---
@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at', 'message_snippet')
    list_filter = ('sent_at',)
    search_fields = ('name', 'email', 'message')
    ordering = ('-sent_at',)
    readonly_fields = ('name', 'email', 'message', 'sent_at') 

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_snippet.short_description = 'Pesan'