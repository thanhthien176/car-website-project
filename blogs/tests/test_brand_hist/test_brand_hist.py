from django.test import TestCase
from django.db import IntegrityError

from cars.tests.helpers import make_brand
from blogs.tests.helpers import make_brand_history

class BrandHistoryTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand(name="Toyota")
        
    def test_slug_auto_generated_from_brand(self):
        history = make_brand_history(brand=self.brand)
        self.assertIn("toyota", history.slug)
        self.assertIn("history", history.slug)
        
    def test_one_to_one_constraint_one_history_per_brand(self):
        make_brand_history(brand=self.brand)
        with self.assertRaises(IntegrityError):
            make_brand_history(brand=self.brand)
            
    def test_get_absolute_url_uses_brand_slug(self):
        history = make_brand_history(brand=self.brand)
        self.assertIn(self.brand.slug, history.get_absolute_url())
        
    def test_str_returns_title(self):
        history = make_brand_history(brand=self.brand, title="Lịch sử Toyota")
        self.assertEqual(str(history), "Lịch sử Toyota")
        
    def test_published_at_auto_set_when_published(self):
        history = make_brand_history(brand=self.brand, is_published=True)
        self.assertIsNotNone(history.published_at)
        
    def test_published_at_left_empty_when_unpublished(self):
        history = make_brand_history(brand=self.brand, is_published=False)
        self.assertIsNone(history.published_at)
        
    
        
    