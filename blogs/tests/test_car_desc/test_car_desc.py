from django.test import TestCase
from django.utils.text import slugify

from cars.tests.helpers import make_brand, make_car_model, make_variant
from blogs.tests.helpers import make_car_description

class CarDesciptionTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand()
        self.car_model = make_car_model(brand=self.brand)
        self.variant = make_variant(car_model=self.car_model)
        
    def test_slug_includes_variant_slug_when_variant_specific(self):
        desc = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Mô tả"
        )
        self.assertIn(self.variant.slug, desc.slug)
        
    def test_slug_includes_car_model_slug_when_shared(self):
        desc = make_car_description(
            car_model=self.car_model, variant=None, title="Mô tả"
        )
        self.assertIn(self.car_model.slug, desc.slug)
        
    def test_same_title_different_car_model_produces_different_slug(self):
        other_model = make_car_model(brand=self.brand, name="Other model")
        desc = make_car_description(
            car_model=self.car_model, variant=None, title="Mo ta"
        )
        other_desc = make_car_description(
            car_model=other_model, variant=None, title="Mo ta"
        )
        self.assertNotEqual(desc.slug, other_desc.slug)
        
    def test_is_primary_scoped_within_same_variant_group(self):
        d1 = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Bài 1", is_primary=True,
        )
        d2 = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Bài 2", is_primary=True,
        )
        d1.refresh_from_db()
        self.assertTrue(d2.is_primary)
        self.assertFalse(d1.is_primary)
        
    def test_is_primary_independent_between_variant_and_shared_group(self):
        variant_desc = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Bài 1", is_primary=True,
        )
        shared_desc = make_car_description(
            car_model=self.car_model, variant=None,
            title="Bài 2", is_primary=True,
        )
        variant_desc.refresh_from_db()
        shared_desc.refresh_from_db()
        self.assertTrue(variant_desc.is_primary)
        self.assertTrue(shared_desc.is_primary)
        
    def test_non_primary_descriptions_unaffected_by_new_primary(self):
        untouched = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="Not Primary", is_primary=False,
        )
        make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="New description", is_primary=True
        )
        untouched.refresh_from_db()
        self.assertFalse(untouched.is_primary)
        
    def test_image_slug_uses_variant_slug_when_present(self):
        desc = make_car_description(
            car_model=self.car_model, variant=self.variant,
            title="title"
        )
        self.assertEqual(desc.image_slug, self.variant.slug)
        
    def test_image_slug_falls_back_to_car_model_slug(self):
        desc = make_car_description(
            car_model=self.car_model, variant=None,
        )
        self.assertEqual(desc.image_slug, self.car_model.slug)
        
    def test_get_absolute_url_with_variant_points_to_variant_detail(self):
        desc = make_car_description(
            car_model=self.car_model, variant=self.variant
        )
        self.assertIn(self.variant.slug, desc.get_absolute_url())
    
    def test_get_absolute_url_without_variant_points_to_car_detail(self):
        desc = make_car_description(
            car_model=self.car_model, variant=None
        )
        self.assertIn(self.car_model.slug, desc.get_absolute_url())