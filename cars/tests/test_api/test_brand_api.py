
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from ..helpers.helper_models import make_brand


class BrandApiListTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('api:brand-list')
        self.brand_toyota = make_brand(name='Toyota', is_active=True)
        self.brand_kia = make_brand(name='Kia', is_active=True)
        self.brand_inactive = make_brand(name='OldBrand', is_active=False)
        
    def test_list_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_return_only_active_brand(self):
        response = self.client.get(self.url)
        names = [b['name'] for b in response.data['results']]
        self.assertIn('Toyota', names)
        self.assertIn('Kia', names)
        self.assertNotIn('OldBrand', names)
        
    def test_list_is_paginated(self):
        res = self.client.get(self.url)
        self.assertIn('count', res.data)
        self.assertIn('results', res.data)
        self.assertIsInstance(res.data['results'], list)
        
    def test_search_by_name(self):
        res = self.client.get(self.url, {'search': 'Toyota'})
        names = [b['name'] for b in res.data['results']]
        self.assertIn('Toyota', names)
        self.assertNotIn('Kia', names)
        
    def test_ordering_by_name(self):
        res = self.client.get(self.url, {'ordering': 'name'})
        names = [b['name'] for b in res.data['results']]
        self.assertEqual(names, sorted(names))
        

class BrandApiDetailTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.brand = make_brand(name='Toyota')
        self.url = reverse('api:brand-detail', kwargs={'pk': self.brand.pk})
        
    def test_detail_return_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_detail_returns_correct_brand(self):
        res = self.client.get(self.url)
        self.assertEqual(res.data['name'], 'Toyota')
        
    def test_detail_nonexistent_slug_return_404(self):
        url = reverse('api:brand-detail', kwargs={'pk': '20000'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        

class BrandApiPermissionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('api:brand-list')
        
    def test_anonymous_can_read(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_anonymous_cannot_post(self):
        res = self.client.post(self.url, {'name': 'NewBrand'}, format='json')
        print(res.data)
        print(res.status_code)
        # ReadOnlyModelViewSet → 405 Method Not Allowed
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        