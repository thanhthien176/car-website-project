from django.test import TestCase
from cars.models import Comparison
from helpers.helper_models import make_variant, make_car_model

class ComparisonTest(TestCase):
    def setUp(self) -> None:
        self.car_model = make_car_model()
        
    def _make_variants(self, count=3):
        return [
            make_variant(car_model=self.car_model, name = f"variant-{i}")
            for i in range(count)
        ]
        
    def test_can_add_car_true_when_less_than_3(self):
        comparison = Comparison.objects.create(session_key = "abc123")
        variants = self._make_variants(count=2)
        comparison.cars.set(variants)
        self.assertTrue(comparison.can_add_car())
        
    def test_can_add_car_false_when_3_cars(self):
        comparison = Comparison.objects.create(session_key = "abc123")
        variants = self._make_variants(count=3)
        comparison.cars.set(variants)
        self.assertFalse(comparison.can_add_car())
        
    def test_str_no_cars(self):
        comparison = Comparison.objects.create(session_key = "empty")
        self.assertIn("Chưa có xe", str(comparison))
        
    def test_str_with_cars(self):
        comparison = Comparison.objects.create(session_key = "cars123")
        v1 = make_variant(car_model=self.car_model, name="2.0G")
        v2 = make_variant(car_model=self.car_model, name="2.0HEV")
        comparison.cars.add(v1)
        comparison.cars.add(v2)        
        self.assertIn("2.0G", str(comparison))
        self.assertIn("2.0HEV", str(comparison))
        
        