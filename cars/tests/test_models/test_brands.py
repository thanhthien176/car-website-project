import pytest
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from cars.models import Brand
from cars.tests.helpers.helper_models import make_brand

class BrandModelTest(TestCase):
    def test_slug_auto_generated_on_create(self):
        brand = make_brand(name="Toyota")
        self.assertEqual(brand.slug, "toyota")
        
    def test_slug_with_spaces_slugified(self):
        brand = make_brand(name="Roll Royce")
        self.assertEqual(brand.slug, "roll-royce")
        
    def test_slug_not_overwritten_if_provided(self):
        brand = make_brand(name="Kia", slug="kia-motors")
        self.assertEqual(brand.slug, "kia-motors")
        
    def test_slug_not_overwritten_on_resave(self):
        brand = make_brand(name="Vinfast")
        original_slug = brand.slug
        brand.founded_year = 1980
        brand.save()
        brand.refresh_from_db()
        self.assertEqual(brand.slug, original_slug)
        
     # ── SEO properties ───────────────────────────────────────────────────
    def test_get_seo_title_fallback(self):
        brand = make_brand(name="Toyota")
        self.assertIn("Toyota",brand.get_seo_title)
        self.assertIn("WebsiteCar", brand.get_seo_title)
        
    def test_get_seo_title_custom(self):
        brand = make_brand(name="Toyota", seo_title="My Custom Title")
        self.assertEqual(brand.get_seo_title, "My Custom Title")
        
    def test_get_seo_description_fallback(self):
        brand = make_brand(name="Toyota", country_of_origin="Japan")
        self.assertIn("Toyota", brand.get_seo_description)
        self.assertIn("Japan", brand.get_seo_description)
        
    def test_get_seo_description_custom(self):
        brand = make_brand(name="Toyota", seo_description="My custom description")
        self.assertEqual(brand.get_seo_description, "My custom description")
        
    def test_str(self):
        brand = make_brand(name="Toyota")
        self.assertEqual(str(brand), "Toyota")
        
    def test_duplicate_name_raises(self):
        brand = make_brand(name="Huyndai")
        with self.assertRaises(IntegrityError):
            make_brand(name="Huyndai")
        
    def test_default_ordering_by_name(self):
        make_brand(name="Huyndai")
        make_brand(name="Kia")
        make_brand(name="Vinfast")
        names = list(Brand.objects.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))
        
        