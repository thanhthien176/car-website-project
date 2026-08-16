from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from cars.models import CarModel
from cars.tests.helpers.helper_models import make_car_model, make_brand

class CarModelTest(TestCase):
    def setUp(self):
        self.brand = make_brand(name="Toyota")
    
    # ── slug ─────────────────────────────────────────────────────────────    
    def test_slug_generated_from_brand_and_name(self):
        car = make_car_model(brand=self.brand, name="Camry")
        self.assertEqual(car.slug, "toyota-camry")
        
    def test_slug_stable_on_resave(self):
        car = make_car_model(brand=self.brand, name="Camry")
        original = car.slug
        car.model_year=2019
        car.save()
        car.refresh_from_db()
        self.assertEqual(car.slug, original)
    
    # ── unique constraint ────────────────────────────────────────────────
    def test_same_brand_same_name_raises(self):
        make_car_model(brand=self.brand, name="Camry")
        with self.assertRaises(IntegrityError):
            make_car_model(brand=self.brand, name="Camry")
    
    def test_same_name_different_brand_ok(self):
        make_car_model(brand=self.brand, name="Civic")
        honda = make_brand(name="Honda")
        car = make_car_model(brand=honda, name="Civic")
        self.assertEqual(car.slug, "honda-civic")
        
    #  ── SEO properties ───────────────────────────────────────────────────
    def test_seo_title_fallback(self):
        car = make_car_model(brand=self.brand, name="Hilux")
        self.assertIn("Hilux", car.get_seo_title)
        self.assertIn("Toyota", car.get_seo_title)
        self.assertIn("Tìm hiểu mẫu xe", car.get_seo_title)
        
    def test_seo_description_fallback(self):
        car = make_car_model(brand=self.brand, name="Innova")
        self.assertIn("Toyota Innova", car.get_seo_description)
        
    # ── __str__ ──────────────────────────────────────────────────────────
    def test_str(self):
        car = make_car_model(brand=self.brand, name="Vios")
        self.assertEqual(str(car), "Toyota Vios")
    
    # ── avg_rating default ───────────────────────────────────────────────
    def test_avg_rating_default_zero(self):
        car = make_car_model(brand=self.brand, name="Vios")
        self.assertEqual(car.avg_rating, Decimal(0))
        
        