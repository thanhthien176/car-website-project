from django.test import TestCase

from blogs.services import get_description_for_variant
from blogs.tests.helpers import make_car_description
from cars.tests.helpers import make_brand, make_car_model, make_variant


class GetDescriptionForVariantTest(TestCase):
    """
    Priority under test:
        1. variant-specific primary (variant=<this>, is_primary=True)
        2. shared car_model-level primary (variant=None, is_primary=True)
        3. None
    Each candidate must also satisfy is_published=True.
    """
    
    def setUp(self) -> None:
        self.brand = make_brand()
        self.car_model = make_car_model(brand=self.brand)
        self.variant = make_variant(car_model=self.car_model)
        
    def test_returns_variant_specific_primary_when_present(self):
        variant_desc = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Riêng cho variant", is_primary=True,
        )
        make_car_description(
            car_model=self.car_model, variant=None,
            title="Dùng chung", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertEqual(result, variant_desc)
    
    def test_falls_back_to_shared_primary_when_no_variant_specific(self):
        shared_desc = make_car_description(
            car_model=self.car_model, variant=None,
            title="Dùng chung", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertEqual(result, shared_desc)
        
    def test_returns_none_when_nothing_matches(self):
        result = get_description_for_variant(self.variant)
        self.assertIsNone(result)
        
    def test_unpublished_variant_specifice_is_ignored(self):
        make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Riêng nhưng chưa publish", is_primary=True, is_published=False,
        )
        shared_desc = make_car_description(
            car_model=self.car_model, variant=None,
            title="Dùng chung", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertEqual(result, shared_desc)
        
    def test_unpublished_shared_is_ignored(self):
        make_car_description(
            car_model=self.car_model, variant=None,
            title="Dùng chung nhưng chưa publish", is_primary=True, is_published=False,
        )
        result = get_description_for_variant(self.variant)
        self.assertIsNone(result)
        
    def test_non_primary_variant_specific_is_ignored(self):
        make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Riêng nhưng không phải primary", is_primary=False,
        )
        shared_desc = make_car_description(
            car_model=self.car_model, variant=None,
            title="Dùng chung", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertEqual(result, shared_desc)
        
    def test_shared_primary_of_a_different_car_model_is_not_returned(self):
        other_model = make_car_model(brand=self.brand, name="Other Model")
        make_car_description(
            car_model=other_model, variant=None,
            title="Dùng chung cho other model", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertIsNone(result)
    
    def test_variant_specific_of_a_different_variant_is_not_returned(self):
        other_variant = make_variant(car_model=self.car_model, name="other variant")
        make_car_description(
            car_model=self.car_model, variant=other_variant,
            title="Riêng của other variant", is_primary=True,
        )
        result = get_description_for_variant(self.variant)
        self.assertIsNone(result)