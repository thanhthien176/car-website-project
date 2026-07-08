from django.contrib import admin

from blogs.models import BlogTag, BlogSection, BlogPost, BlogCategory

class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1
    fields = ["order", "title", "content", "image"]
    
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    
@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    
    
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "is_published", "published_at"]
    list_filter = ["is_published", "category", "tags"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [BlogSectionInline]



