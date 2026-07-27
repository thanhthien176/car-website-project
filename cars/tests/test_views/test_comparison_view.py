from django.test import TestCase
from django.urls import reverse

from cars.tests.helpers.helper_models import make_car_model, make_variant
from cars.models import Comparison

class AddToComparisonViewTest(TestCase):
    def setUp(self) -> None:
        self.car_model = make_car_model()
        self.v1 = make_variant(car_model=self.car_model, name='2.0G')
        self.v2 = make_variant(car_model=self.car_model, name='2.5G')
        self.v3 = make_variant(car_model=self.car_model, name='3.0G')
        self.v4 = make_variant(car_model=self.car_model, name='3.5G')
        
    def _add_url(self, variant_pk):
        return reverse('cars:comparison_add', kwargs={'variant_pk': variant_pk})
    
    def test_add_creates_comparison_with_session_key(self):
        response = self.client.post(self._add_url(self.v1.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comparison.objects.count(), 1)
        comparison = Comparison.objects.first()
        self.assertEqual(comparison.session_key, self.client.session.session_key)
        
    def test_add_returns_correct_count(self):
        response = self.client.post(self._add_url(self.v1.pk))
        data = response.context
        self.assertEqual(data['total'], 1)
        
    def test_add_same_variant_twice_returns_already_added(self):
        self.client.post(self._add_url(self.v1.pk))
        response = self.client.post(self._add_url(self.v1.pk))
        data = response.context
        self.assertEqual(data['status'], 'already_added')
        self.assertEqual(Comparison.objects.first().cars.count(), 1)
        
    def test_add_fourth_car_returns_limit_reached(self):
        self.client.post(self._add_url(self.v1.pk))
        self.client.post(self._add_url(self.v2.pk))
        self.client.post(self._add_url(self.v3.pk))
        response = self.client.post(self._add_url(self.v4.pk))
        data = response.context
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['status'], 'limit_reached')
    
    def test_add_inactive_variant_return_404(self):
        self.v1.is_active = False
        self.v1.save()
        response = self.client.post(self._add_url(self.v1.pk))
        self.assertEqual(response.status_code, 404)
        
class RemoveFromComparisonViewTest(TestCase):
    def setUp(self) -> None:
        self.car_model = make_car_model()
        self.v1 = make_variant(car_model=self.car_model, name='2.0G')
        
    def _add_url(self, variant_pk):
        return reverse('cars:comparison_add', kwargs={'variant_pk': variant_pk})
    
    def _remove_url(self, variant_pk):
        return reverse('cars:comparison_remove', kwargs={'variant_pk': variant_pk})
    
    def test_remove_non_existing_relation(self):
        response = self.client.post(self._remove_url(self.v1.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["status"], "removed")
        
    def test_remove_existing_variant(self):
        self.client.post(self._add_url(self.v1.pk))
        comparison = Comparison.objects.first()
        self.assertEqual(comparison.cars.count(), 1)
        response = self.client.post(self._remove_url(self.v1.pk))
        self.assertEqual(response.status_code, 200)
        comparison = Comparison.objects.first()
        self.assertEqual(comparison.cars.count(), 0)
        
        
        
        
        
        

