from django.contrib import admin

from blogs.models import BrandHistorySection, BrandHistory


class BrandHistorySectionInline(admin.TabularInline):
    model = BrandHistorySection
    extra = 1
    fields = ["order", "title", "content", "image"]
    

@admin.register(BrandHistory)
class BrandHistoryAdmin(admin.ModelAdmin):
    list_display = ["brand", "title", "is_published", "published_at"]
    list_filter = ["is_published"]
    search_fields = ["brand__name", "title"]
    autocomplete_fields = ["brand"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [BrandHistorySectionInline]
    
    