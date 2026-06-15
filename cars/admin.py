import csv

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse


from .models import (
    Brand, CarModel, CarVariant, CarImage, VariantImage,
    DimensionSpecification, EngineSpecification, PerformanceSpecification,
    FuelConsumptionSpecification, ExteriorSpecification, InteriorSpecification,
    SeatSpecification, ComfortSpecification, SafetySpecification,
    Review, Comparison,
)

# Register your models here.

# ======= Export cars CSV =======
def export_cars_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="cars-export.csv"'
    response.write('\ufeff')  # BOM for Excel UTF-8 compatibility
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Brand', 'Model', 'Variant', 'Year',
        'Body Type', 'Fuel Type', 'Price Min', 'Price Max', 
        'Avg Rating', 'Is Active',        
    ])
    
    qs = queryset.select_related(
        "car_model__brand",
        "car_model__body_type",
    )
    
    for variant in qs:
        model = variant.car_model
        writer.writerow([
            variant.id,
            model.brand.name,
            model.name,
            variant.variant_name,
            model.model_year or "",
            model.body_type.name if model.body_type else "",
            variant.get_fuel_type_display(),
            variant.price_min/1_000_000,
            variant.price_max/1_000_000,
            model.avg_rating,
            "Yes" if variant.is_active else "No",
        ])
        
    return response

export_cars_csv.short_description = "Export selected variants to CSV"

# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ['image', 'caption', 'is_primary', 'order']
    
class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 2
    fields = ['image', 'caption', 'is_primary', 'order']
    
    
# The specifications are split into 9 separate models — each requiring its own inline.
class DimensionSpecInline(admin.StackedInline):
    model = DimensionSpecification
    can_delete = False
    verbose_name_plural = "Kích thước"
    
class EngineSpecInline(admin.StackedInline):
    model = EngineSpecification
    can_delete = False
    verbose_name_plural = "Động cơ & Hộp số"
 
 
class PerformanceSpecInline(admin.StackedInline):
    model = PerformanceSpecification
    can_delete = False
    verbose_name_plural = "Vận hành"
 
 
class FuelConsumptionSpecInline(admin.StackedInline):
    model = FuelConsumptionSpecification
    can_delete = False
    verbose_name_plural = "Mức tiêu thụ nhiên liệu"
 
 
class ExteriorSpecInline(admin.StackedInline):
    model = ExteriorSpecification
    can_delete = False
    verbose_name_plural = "Ngoại thất"
 
 
class InteriorSpecInline(admin.StackedInline):
    model = InteriorSpecification
    can_delete = False
    verbose_name_plural = "Nội thất"
 
 
class SeatSpecInline(admin.StackedInline):
    model = SeatSpecification
    can_delete = False
    verbose_name_plural = "Ghế ngồi"
 
 
class ComfortSpecInline(admin.StackedInline):
    model = ComfortSpecification
    can_delete = False
    verbose_name_plural = "Tiện nghi"
 
 
class SafetySpecInline(admin.StackedInline):
    model = SafetySpecification
    can_delete = False
    verbose_name_plural = "An toàn"
    
# ---------------------------------------------------------------------------
# Custom filters
# ---------------------------------------------------------------------------
 
class PriceRangeFilter(admin.SimpleListFilter):
    title = "Khoảng giá"
    parameter_name = "price_range"
 
    def lookups(self, request, model_admin):
        return [
            ("under_500",  "Dưới 500 triệu"),
            ("500_1000",   "500 triệu – 1 tỷ"),
            ("1000_2000",  "1 tỷ – 2 tỷ"),
            ("over_2000",  "Trên 2 tỷ"),
        ]
 
    def queryset(self, request, queryset):
        v = self.value()
        # BUG FIX #9: "over_2000" dùng price_min__lt: 2000 — ngược logic.
        # Phải là price_min__gte: 2000.
        map_filter = {
            "under_500":  {"price_min__lt": 500},
            "500_1000":   {"price_min__gte": 500,  "price_min__lt": 1000},
            "1000_2000":  {"price_min__gte": 1000, "price_min__lt": 2000},
            "over_2000":  {"price_min__gte": 2000},   # ← đã sửa
        }
        f = map_filter.get(v) if v else None
        return queryset.filter(**f) if f else queryset

class RatingFilter(admin.SimpleListFilter):
    title = "Rating"
    parameter_name = "rating"
 
    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin):
        return [
            ("high",      "Cao (≥ 4.0)"),
            ("medium",    "Trung bình (2.0 – 3.9)"),
            ("low",       "Thấp (< 2.0)"),
            ("no_review", "Chưa có đánh giá"),
        ]
 
    def queryset(self, request, queryset) -> QuerySet | None:
        v = self.value()
        map_filter = {
            "high":      {"avg_rating__gte": 4},
            "medium":    {"avg_rating__gte": 2, "avg_rating__lt": 4},
            "low":       {"avg_rating__gt": 0,  "avg_rating__lt": 2},
            "no_review": {"avg_rating": 0},
        }
        f = map_filter.get(v) if v else None
        return queryset.filter(**f) if f else queryset
    
# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------
 
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display  = ['name', 'country_of_origin', 'founded_year', 'is_active']
    list_filter   = ['is_active', 'country_of_origin']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

# ---------------------------------------------------------------------------
# CarModel
# ---------------------------------------------------------------------------
 
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'brand', 'body_type', 'model_year', 'avg_rating']
    list_filter   = ['brand', 'body_type', 'car_class', RatingFilter]  
    search_fields = ['name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['avg_rating']
    
    inlines = [
        CarImageInline,
    ]


# ---------------------------------------------------------------------------
# CarVariant
# ---------------------------------------------------------------------------

@admin.register(CarVariant)
class CarVariantAdmin(admin.ModelAdmin):

    list_display = [
    '__str__', 'get_brand', 'get_body_type',

    'fuel_type', 'price_min', 'price_max', 'is_active',

    ]

    list_filter = [
    'car_model__brand',

    'car_model__body_type',

    'fuel_type',

    'is_active',

    PriceRangeFilter,

    ]

    search_fields = ['name', 'car_model__name', 'car_model__brand__name']

    prepopulated_fields = {'slug': ('name',)}

    list_editable = ['is_active']
    
    actions = [export_cars_csv] 

    inlines = [ 
    VariantImageInline, 
    DimensionSpecInline, 
    EngineSpecInline, 
    PerformanceSpecInline, 
    FuelConsumptionSpecInline, 
    ExteriorSpecInline, 
    InteriorSpecInline, 
    SeatSpecInline, 
    ComfortSpecInline, 
    SafetySpecInline, 
    ] 

# --- helper display methods ------------------------------------------- 

    @admin.display(description="Car brand", ordering='car_model__brand__name') 
    def get_brand(self, obj): 
        return obj.car_model.brand 

    @admin.display(description="Vehicle type", ordering='car_model__body_type__name') 
    def get_body_type(self, obj): 
        return obj.car_model.body_type
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['author_name', 'car', 'rating', 'is_approved', 'created_at']
    list_filter   = ['is_approved', 'rating']
    search_fields = ['author_name', 'car__name']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']

