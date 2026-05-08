from collections.abc import Iterable
from typing import Any

from django.contrib import admin
from django.db.models import Avg, Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
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
    
# SimplelistFilter
class PriceRangeFilter(admin.SimpleListFilter):
    title = "Khoảng giá"
    parameter_name = "price_range"
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("under_500", "Dưới 500 triệu"),
            ("500_1000", "500 Triệu - 1 tỷ"),
            ("1000_2000", "1 tỷ - 2 tỷ"),
            ("over_2000", "Trên 2 tỷ")
        ]
        
    def queryset(self, request: Any, queryset):
        v = self.value()
        map_filter = {
            "under_500": {"price_min__lt":500},
            "500_1000": {"price_min__gte": 500, "price_min__lt": 1000},
            "1000_2000": {"price_min__gte": 1000, "price_min__lt": 2000},
            "over_2000": {"price_min__lt": 2000},
        }
        
        filter = map_filter.get(v) if v else None
        
        if filter:
            return queryset.filter(**filter)
        
        return queryset
    
class RatingFilter(admin.SimpleListFilter):
    title = "Rating"
    parameter_name = "rating"
    
    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin):
        return [
            ("high", "Cao (>= 4.0)"),
            ("medium", "Trung bình (2.0-3.9)"),
            ("low", "Thấp (<= 2.0)"),
            ("no_review","Chưa có đánh giá"),            
        ]
        
    def queryset(self, request, queryset) -> QuerySet | None:
        v = self.value()
        map_filter = {
            "high": {"avg_rating__gte": 4},
            "medium": {"avg_rating__lt": 4, "avg_rating__gte": 2},
            "low": {"avg_rating__lt": 2, "avg_rating__gt": 0},
            "no_review": {"avg_rating": 0}
        }
        
        filter = map_filter.get(v) if v else None
        
        if filter:
            return queryset.filter(**filter)
        
        return queryset
    
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'body_type', 'fuel_type', 'price_min', 'price_max', 'is_featured', 'is_active']
    list_filter = ['brand', 'body_type', 'fuel_type', 'transmission', 'is_active', 'is_featured', PriceRangeFilter, RatingFilter]
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
    actions = ['approve_reviews', 'reject_reviews']
    
    @admin.action(description="Approve review")
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"Đã duyệt {updated} reviews")
        
    @admin.action(description="Reject review")
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"Đã từ chối {updated} reviews")
    
@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ['__str__','car_count', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['cars']
    
    @admin.display(description="Car count")
    def car_count(self, obj):
        return obj.cars.count()
    


        
