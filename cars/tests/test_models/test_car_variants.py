import pytest
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from cars.models import CarVariant
from helpers.helper_models import make_variant, make_brand, make_car_model

class CarVariantTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand(name="Toyota")
        self.car_model = make_car_model(brand=self.brand, name="Innova")
        
    # ── slug ─────────────────────────────────────────────────────────────
    def test_slug_generated_from_car_and_variant(self):
        variant = make_variant(car_model=self.car_model, variant_name="Cross 2.0G")
        self.assertEqual(variant.slug, "toyota-innova-cross-20g")
        
    # ── price_range property ─────────────────────────────────────────────
    def test_price_range_format(self):
        variant = make_variant(
            car_model=self.car_model,
            variant_name="Cross 2.0HEV",
            price_min=930_000_000,
            price_max=1_100_000_000,
            )
        result = variant.price_range
        self.assertIn("triệu VNĐ", result)
        self.assertIn("930", result)
        self.assertIn("1,100", result)
    
    # ── primary_image property ───────────────────────────────────────────
    def test_primary_image_when_no_image(self):
        variant = make_variant(car_model=self.car_model, variant_name="Cross 2.0HEV")
        self.assertIsNone(variant.primary_image)
        
    # ── unique constraint ────────────────────────────────────────────────
    def test_duplicate_variant_name_under_same_model_raise(self):
        variant = make_variant(car_model=self.car_model, variant_name="Cross 2.0HEV")
        with self.assertRaises(IntegrityError):
            make_variant(car_model=self.car_model, variant_name="Cross 2.0HEV")
            
    def test_same_variant_name_different_model_ok(self):
        model = make_car_model(brand=self.brand, name="Hilux")
        v1 = make_variant(car_model=self.car_model, variant_name="Cross 2.0G")
        v2 = make_variant(car_model=model, variant_name="Cross 2.0G")
        self.assertNotEqual(v1.slug, v2.slug)
        
     # ── fuel_type choices ────────────────────────────────────────────────
    def test_valid_fuel_type_choices(self):
        valid_fuels = [c[0] for c in CarVariant.FUEL_TYPE_CHOICES]
        for fuel in valid_fuels:
            variant = make_variant(
                car_model=self.car_model,
                variant_name=f"fuel {fuel}",
                fuel_type=fuel,
                )
            self.assertEqual(variant.fuel_type, fuel)
            
    # ── __str__ ──────────────────────────────────────────────────────────
    def test_str(self):
        variant = make_variant(car_model=self.car_model, variant_name="Cross 2.0G")
        self.assertEqual(str(variant),"Toyota Innova Cross 2.0G")
        
    # ── SEO meta ─────────────────────────────────────────────────────────
    def test_get_meta_title_fallback(self):
        variant = make_variant(car_model=self.car_model, variant_name="Cross 2.0G")
        self.assertIn("Cross 2.0G", variant.get_meta_title())
        self.assertIn("Toyota Innova", variant.get_meta_title())
        self.assertIn("WebsiteCar", variant.get_meta_title())
        
    def test_get_meta_title_custom_seo(self):
        variant = make_variant(
            car_model=self.car_model,
            variant_name="Cross 2.0G",
            seo_title="Custom SEO"
        )
        self.assertEqual(variant.get_meta_title(), "Custom SEO")
        
    def test_get_meta_description_custom_seo(self):
        variant = make_variant(
            car_model=self.car_model,
            variant_name="Cross 2.0G",
            seo_description="Custom Description SEO"
        )     
        self.assertEqual(variant.get_meta_description(), "Custom Description SEO")             
             