from rest_framework import serializers
from django.db.models import Count
from cars.models import Brand, CarModel, CarVariant

class BrandSerializers(serializers.ModelSerializer):
    """
     Read-only serializer for Brand.
    Expects the queryset to be annotated with `car_model_count`
    via annotate(car_model_count=Count('car_models')).
    The SerializerMethodField fallback below is for safety only —
    it will cause N+1 if the annotation is missing.
    """
    # SerializerMethodField: computed field, read-only.
    
    # DRF will automatically call the get_<field_name>(self, obj) method when serialize
    car_model_count = serializers.IntegerField(read_only=True, default=0)
    
    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'country_of_origin',
            'founded_year', 'website', 'logo',
            'is_active', 'car_model_count',
        ]
        read_only_fields = ['slug']
        
    def get_car_model_count(self, obj):
        """
        Return the number car_models for this brand
        """
        return obj.car_models.annotate(car_model_count=Count('car_models'))


class CarModelSerializers(serializers.ModelSerializer):
    """ 
    Serializers for CarModel
    Nests BrandSerializers for brand info - requires select_related('brand')
    in the ViewSet queryset to avoid N+1.
    Expects annotate: variant_count=Count('variants').
    """
    brand = BrandSerializers()
    variant_count = serializers.IntegerField(read_only=True, default=0)
    
    class Meta:
        model = CarModel
        fields = [
            'id', 'name', 'slug', 'brand',
            'body_type', 'model_year', 'avg_rating',
            'variant_count',
        ]
        read_only_fields = ['slug', 'avg_rating']
        
    def get_variant_count(self, obj):
        """
        Return the number of variants for this car model
        """
        return obj.objects.annotate(variant_count=Count('variants'))
    
class CarVariantSerializers(serializers.ModelSerializer):
    """ 
     Serializer for CarVariant.
    - car_model: nested for name/slug access
    - brand_name: flattened from car_model.brand to avoid deep nesting
    - price_range: read from model property directly
    - primary_image: read from model property directly
    Requires: select_related('car_model__brand', 'car_model__body_type')
    """
    
    car_model = CarModelSerializers(read_only=True)
    
    # Flattened field: read nested attribute via dot
    # source='car_model.brand.name' → DRF traverse each attribute
    brand_name = serializers.CharField(source='car_model.brand.name', read_only=True)
    
    # Model properties — DRF reads like a normal attribute
    price_range = serializers.CharField(read_only=True)
    primary_image = serializers.CharField(read_only=True, allow_null=True)
    
    class Meta:
        model = CarVariant
        fields = [
            'id', 'variant_name', 'slug',
            'car_model', 'brand_name',
            'fuel_type', 'price_min', 'price_max', 'price_range',
            'is_active', 'primary_image',
        ]

        read_only_fields = ['slug']
    