from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from ..helpers.helper_models import make_brand, make_car_model, make_variant

class CarModelApiListTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('api:car-list')
        self.toyota = make_brand(name='Toyota')
        self.honda = make_brand(name='Honda')
        self.camry = make_car_model(brand=self.toyota, name='Camry')
        self.civic = make_car_model(brand=self.honda, name='Civic')
        
    def test_list_returns_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_list_is_paginated(self):
        res = self.client.get(self.url)
        self.assertIn('count', res.data)
        self.assertIn('results', res.data)
        
    def test_list_contains_all_models(self):
        res = self.client.get(self.url)
        names = [m['name'] for m in res.data['results']]
        self.assertIn('Civic', names)
        self.assertIn('Camry', names)
        
    def test_search_by_model_name(self):
        res = self.client.get(self.url, {'search': 'Camry'})
        names = [m['name'] for m in res.data['results']]
        self.assertIn('Camry', names)
        self.assertNotIn('Civic', names)
        
    def test_search_by_brand_name(self):
        res = self.client.get(self.url, {'search': 'Honda'})
        names = [m['name'] for m in res.data['results']]
        self.assertIn('Civic', names)
        self.assertNotIn('Camry', names)
    
    def test_filter_by_brand_slug(self):
        res = self.client.get(self.url, {'brand': self.toyota.slug})
        names = [m['name'] for m in res.data['results']]
        self.assertIn('Camry', names)
        self.assertNotIn('Civic', names)


class CarModelApiDetailTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.toyota = make_brand(name='Toyota')
        self.camry = make_car_model(brand=self.toyota, name='Camry')
        self.url = reverse('api:car-detail', kwargs={'pk': self.camry.pk})
        
    def test_detail_returns_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_detail_returns_correct_model(self):
        res = self.client.get(self.url)
        self.assertEqual(res.data['name'], 'Camry')
        
    def test_detail_contains_brand_info(self):
        res = self.client.get(self.url)
        self.assertEqual(res.data['brand']['name'], 'Toyota')
        
    def test_detail_contains_variant_count(self):
        make_variant(car_model=self.camry, name='2.0G')
        make_variant(car_model=self.camry, name='2.5Q')
        res = self.client.get(self.url)
        self.assertEqual(res.data['variant_count'], 2)
        
    def test_detail_nonexistent_pk_returns_404(self):
        url = reverse('api:car-detail', kwargs={'pk': 20})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)