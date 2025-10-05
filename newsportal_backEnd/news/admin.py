# D:\ne

# newsportal_backEnd/news/admin.py

from django.contrib import admin
# Import all necessary models
from .models import Article, Category, Location, Image, Video , Comment
# We remove the LLM service import since we removed its target fields/action

# --- 1. Inline Definitions (Embeds Image/Video in ArticleAdmin) ---

class ImageInline(admin.StackedInline): # StackedInline for vertical layout
    model = Image
    extra = 1 # Show 1 extra empty form by default

class VideoInline(admin.StackedInline):
    model = Video
    extra = 1

# --- 2. Article Admin (The Main Registration) ---

# We only keep the ArticleAdmin, and remove the @admin.register(Image/Video) 
# since they are now managed as inlines.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Field ordering in the form
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'location')
        }),
        ('Content', {
            'fields': ('short_description', 'detailed_description')
        }),
    )

    list_display = ('title', 'category', 'location', 'publication_date')
    list_filter = ('category', 'location', 'publication_date')
    search_fields = ('title', 'short_description')
    
    # Add the Inlines here!
    inlines = [ImageInline, VideoInline]
    
    # REMOVED: The actions = [generate_ai_content] line is gone!

# --- 3. Separate Registration for Category and Location ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author_name', 'content')