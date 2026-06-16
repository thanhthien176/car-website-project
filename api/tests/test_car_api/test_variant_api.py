from decimal import Decimal
from os import name

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

from cars.tests.helpers.helper_models import make_brand, make_car_model, make_variant

class CarVariantApiListTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('api:variant-list')
        self.brand = make_brand(name='Toyota')
        self.camry = make_car_model(brand=self.brand, name='Camry')
        self.v1 = make_variant(
            car_model=self.camry,
            name='2.5Q',
            fuel_type='gasoline',
            price_min=Decimal("1_100_000_000"),
            price_max=Decimal("1_200_000_000")
        )
        self.v2 = make_variant(
            car_model=self.camry,
            name='2.5HEV',
            fuel_type='hybrid',
            price_min=Decimal("1_500_000_000"),
            price_max=Decimal("1_600_000_000")
        )
        self.v_inactive = make_variant(
            car_model=self.camry,
            name='OldTrim',
            fuel_type='gasoline',
            price_min=Decimal("900_000_000"),
            price_max=Decimal("950_000_000"),
            is_active=False
        )
    
    def test_list_returns_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_list_is_paginated(self):
        res = self.client.get(self.url)
        self.assertIn('count', res.data)
        self.assertIn('results', res.data)
        
    def test_list_excludes_inactive_variants(self):
        res = self.client.get(self.url)
        names = [v['name'] for v in res.data['results']]
        self.assertNotIn('OldTrim', names)
        
    def test_filter_by_fuel_type(self):
        res = self.client.get(self.url, {'fuel_type': 'hybrid'})
        names = [v['name'] for v in res.data['results']]
        self.assertNotIn('2.5Q', names)
        self.assertIn('2.5HEV', names)
        
    def test_filter_price_min(self):
        res = self.client.get(self.url, {'price_min': 1_400_000_000})
        names = [v['name'] for v in res.data['results']]
        self.assertIn('2.5HEV', names)
        self.assertNotIn('2.5Q', names)
        
    def test_filter_price_max(self):
        res = self.client.get(self.url, {'price_max': 1_300_000_000})
        names = [v['name'] for v in res.data['results']]
        self.assertIn('2.5Q', names)
        self.assertNotIn('2.5HEV', names)
        
    def test_filter_price_range(self):
        res = self.client.get(self.url, {
            'price_min': 1_000_000_000,
            'price_max': 1_300_000_000,
        })
        names = [v['name'] for v in res.data['results']]
        self.assertIn('2.5Q', names)
        self.assertNotIn('2.5HEV', names)
        

class CarVariantApiDetailTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.brand = make_brand(name='Toyota')
        self.camry = make_car_model(brand=self.brand, name='Camry')
        self.variant = make_variant(
            car_model=self.camry,
            name='2.5Q',
            fuel_type='gasoline',
            price_min=Decimal('1_100_000_000'),
            price_max=Decimal('1_200_000_000')
        )
        self.url = reverse('api:variant-detail', kwargs={'pk': self.variant.pk})
    
    def test_detail_returns_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_detail_returns_correct_variant(self):
        res = self.client.get(self.url)
        self.assertEqual(res.data['name'], '2.5Q')
        
    def test_detail_contains_car_model_info(self):
        res = self.client.get(self.url)
        self.assertEqual(res.data['car_model']['name'], 'Camry')
        
    def test_detail_contains_price_fields(self):
        res = self.client.get(self.url)
        self.assertIn('price_min', res.data)
        self.assertIn('price_max', res.data)
        
    def test_detail_nonexistent_pk_returns_404(self):
        url = reverse('api:variant-detail', kwargs={'pk': '-2'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
            