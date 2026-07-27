from django.test import TestCase
from django.urls import reverse

from cars.tests.helpers.helper_models import make_brand

class BrandListViewTest(TestCase):
    
    def setUp(self) -> None:
        self.url = reverse('cars:brand_list')
        self.brand_active = make_brand(name='Toyota', is_active=True)
        self.brand_inactive = make_brand(name='OldBrand', is_active=False)
        
    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cars/brands/brand_list.html')
        
    def test_only_active_brands_in_context(self):
        response = self.client.get(self.url)
        brands = response.context['brands']
        self.assertIn(self.brand_active, brands)
        self.assertNotIn(self.brand_inactive, brands)
        
class BrandDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand(name="Toyota", is_active=True)
        self.url = reverse('cars:brand_detail', kwargs={'slug': self.brand.slug})
        
    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_404_for_inactive_brand(self):
        inactive = make_brand(name="OldBrand", is_active=False)
        url = reverse('cars:brand_detail', kwargs={'slug': inactive.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_404_in_nonexistent_slug(self):
        url = reverse('cars:brand_detail', kwargs={'slug': 'does-not-exist'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_brand_in_context(self):
        response = self.client.get(self.url)
        self.assertEqual(self.brand, response.context['brand'])    
    