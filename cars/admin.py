from django.contrib import admin
from .models import Brand, Car, CarImage, CarSpecification, Review, Comparison

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
    
    
@admin.action(description="Approve review")
def approve_reviews(modeladmin, request, queryset):
    updated = queryset.update(is_approved=True)
    modeladmin.message_user(request, f"Đã duyệt {updated} reviews")
    
@admin.action(description="Reject review")
def reject_reviews(modeladmin, request, queryset):
    updated = queryset.update(is_approved=False)
    modeladmin.message_user(request, f"Đã từ chối {updated} reviews")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'car', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    list_editable = ['is_approved']
    search_fields = ['author_name', 'car__name', 'title']
    readonly_fields = ['created_at']
    actions = [approve_reviews, reject_reviews]
    
@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ['__str__','car_count', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['cars']
    
    @admin.display(description="Car count")
    def car_count(self, obj):
        return obj.cars.count()