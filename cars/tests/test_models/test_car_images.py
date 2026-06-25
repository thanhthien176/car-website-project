import pytest
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from cars.models import CarImage
from cars.tests.helpers.helper_models import make_car_model

class CarImageTest(TestCase):
    def setUp(self) -> None:
        self.car_model = make_car_model()
        
    def _make_image(self, is_primary=False, order=0):
        img = CarImage(car=self.car_model, is_primary=is_primary, order=order)
        img.image.name = f"car/gallery/test-{order}.webp"
        img.save()
        return img
    
    def test_only_one_primary_image_per_variant(self):
        img1 = self._make_image(is_primary=True, order=1)
        img2 = self._make_image(is_primary=True, order=2)
        img1.refresh_from_db()
        self.assertFalse(img1.is_primary)
        self.assertTrue(img2.is_primary)
        
    def test_non_primary_images_unaffected(self):
        img1 = self._make_image(is_primary=False, order=1)
        img2 = self._make_image(is_primary=False, order=2)
        img1.refresh_from_db()
        self.assertFalse(img1.is_primary)
        self.assertFalse(img2.is_primary)
        
    def test_ordering_by_order_field(self):
        self._make_image(is_primary=False, order=1)
        self._make_image(is_primary=False, order=3)
        self._make_image(is_primary=False, order=2)
        orders=list(CarImage.objects.filter(car=self.car_model).values_list("order", flat=True))
        self.assertEqual(orders, [1,2,3])
        
        