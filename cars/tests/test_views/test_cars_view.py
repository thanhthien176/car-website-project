from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from cars.tests.helpers.helper_models import make_brand, make_car_model, make_variant

class CarModelListViewTest(TestCase):
    
    def setUp(self) -> None:
        cache.clear()
        self.url = reverse('cars:car_list')
        self.toyota = make_brand(name='Toyota')
        self.honda = make_brand(name='Honda')
        self.camry = make_car_model(brand=self.toyota, name='Camry')
        self.civic = make_car_model(brand=self.honda, name='Civic')
        self.v_camry = make_variant(
                    car_model=self.camry,
                    price_min=800_000_000,
                    is_active=True,
                )
        self.v_civic = make_variant(
                    car_model=self.civic,
                    price_min=950_000_000,
                    is_active=True,
                )
        
    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_all_models_shown_without_filter(self):
        response = self.client.get(self.url)
        qs = response.context['car_models']
        self.assertIn(self.camry, qs)
        self.assertIn(self.civic, qs)
        
    def test_search_by_name(self):
        response = self.client.get(self.url, {'q': 'Camry'})
        qs = response.context['car_models']
        self.assertIn(self.camry, qs)
        self.assertNotIn(self.civic, qs)
        
    def test_search_by_brand(self):
        response = self.client.get(self.url, {'q': 'Honda'})
        qs = response.context['car_models']
        self.assertIn(self.civic, qs)
        self.assertNotIn(self.camry, qs)
        
    def test_filter_by_brand_slug(self):
        response = self.client.get(self.url, {'q': self.toyota.slug})
        qs = response.context['car_models']
        self.assertIn(self.camry, qs)
        self.assertNotIn(self.civic, qs)
        
    def test_empty_search_return_all(self):
        response = self.client.get(self.url, {'q': ''})
        qs = response.context['car_models']
        self.assertIn(self.camry, qs)
        self.assertIn(self.civic, qs)
        self.assertEqual(qs.count(), 2)
        
    def test_filter_min_price(self):
        response = self.client.get(self.url, {'min_price': 900})
        qs = response.context['car_models']
        self.assertIn(self.civic, qs)
        self.assertNotIn(self.camry, qs)
        
    def test_filter_max_price(self):
        response = self.client.get(self.url, {'max_price': 900})
        qs = response.context['car_models']
        self.assertIn(self.camry, qs)
        self.assertNotIn(self.civic, qs)
        
    def test_htmx_request_returns_patial(self):
        response = self.client.get(
            self.url,
            {'q': 'Camry'},
            HTTP_HX_REQUEST='true', #simulate HTMX header
        )
        self.assertEqual(response.status_code, 200)
        # Partial doesn't have <html> tag
        self.assertNotContains(response, '<html')
        # But has the car data
        self.assertContains(response, 'Camry')
        
    def test_normal_request_returns_full_page(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<html')
        

