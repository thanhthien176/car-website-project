from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from cars.tests.helpers.helper_models import make_brand, make_car_model, make_variant
from cars.models import Review

class CarVariantDetailViewTest(TestCase):
    
    def setUp(self) -> None:
        cache.clear()
        self.brand = make_brand(name='Toyota')
        self.car_model = make_car_model(brand=self.brand, name='Innova')
        self.variant = make_variant(car_model=self.car_model, name='2.0G')
        self.url = reverse('cars:variant_detail', kwargs={'slug': self.variant.slug})
        
    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_variant_in_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['variant'], self.variant)
        
    def test_other_variants_excludes_self(self):
        sibling = make_variant(car_model=self.car_model, name='2.5Q')
        response = self.client.get(self.url)
        other_variants = response.context['other_variants']
        self.assertIn(sibling, other_variants)
        self.assertNotIn(self.variant, other_variants)
        
    def test_reviews_only_approved(self):
        approved = Review.objects.create(
            car=self.car_model, author_name='A', rating=5,
            title='Good', content='Good', is_approved=True
        )
        
        unapproved = Review.objects.create(
            car=self.car_model, author_name='B', rating=2,
            title='Bad', content='Bad', is_approved=False
        )
        
        response = self.client.get(self.url)
        reviews = response.context['reviews']
        self.assertIn(approved, reviews)
        self.assertNotIn(unapproved, reviews)
        
    def test_404_for_nonexistent_slug(self):
        url = reverse('cars:variant_detail', kwargs={'slug': 'nonexistent-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
          
    