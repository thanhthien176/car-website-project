from django.contrib import admin
from .models import Brand, Car, CarImage, CarSpecification, Review

# Register your models here.
class CarSpecificationInline(admin.StackedInline):
    model = CarSpecification
    can_delete = False

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ['image', 'caption', 'is_primary', 'order']
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_of_origin', 'founded_year', 'is_active']
    list_filter = ['is_active', 'country_of_origin']
    search_field = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'body_type', 'fuel_type', 'price_min', 'price_max', 'is_featured', 'is_active']
    list_filter = ['brand', 'body_type', 'fuel_type', 'transmission', 'is_active', 'is_featured']
    search_fields = ['name','brand__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    inlines = [CarSpecificationInline, CarImageInline]
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'car', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    list_editable = ['is_approved']
    search_fields = ['author_name', 'car__name', 'title']
    readonly_fields = ['created_at']
    

    