from django.contrib import admin

from blogs.models import CarDescription, CarDescriptionSection

class CarDescriptionSectionInline(admin.TabularInline):
    model = CarDescriptionSection
    extra = 1
    fields = ["order", "title", "content", "image"]
    

@admin.register(CarDescription)
class CarDescriptionAdmin(admin.ModelAdmin):
    list_display = ["title", "car_model", "variant", "is_primary", "is_published", "published_at"]
    list_filter = ["is_primary", "is_published", "car_model__brand"]
    search_fields = ["title", "car_model__name", "variant__name"]
    autocomplete_fields = ["car_model", "variant"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CarDescriptionSectionInline]