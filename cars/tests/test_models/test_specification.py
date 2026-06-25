from django.test import TestCase
from django.db import IntegrityError

from cars.models import (
    CarVariant,
    DimensionSpecification,
    EngineSpecification,
    SafetySpecification
    )
from cars.tests.helpers.helper_models import make_car_model, make_variant

class SpecificationModelTest(TestCase):
    def setUp(self) -> None:
        self.variant = make_variant()
        
    def test_dimension_spec_created(self):
        spec = DimensionSpecification.objects.create(
            variant=self.variant,
            length=4885,
            width=1840,
            height=1445,
            wheelbase=2825,
            seating_capacity=5,
        )
        self.assertEqual(spec.length, 4885)
        self.assertEqual(spec.width, 1840)
        self.assertEqual(spec.wheelbase, 2825)
        self.assertEqual(spec.seating_capacity, 5)
        
    def test_dimension_spec_one_to_one_constraint(self):
        DimensionSpecification.objects.create(variant=self.variant)
        with self.assertRaises(IntegrityError):
            DimensionSpecification.objects.create(variant=self.variant)
            
    def test_engine_spec_transmission_choices(self):
        valid_choices = [c[0] for c in EngineSpecification.TRANSMISSION_CHOICES]
        for choice in valid_choices:
            variant = make_variant(
                car_model=self.variant.car_model,
                name = f"variant-{choice}"
            )
            spec = EngineSpecification(
                variant=variant,
                transmission = choice,
            )
            self.assertEqual(spec.transmission, choice)
            
    def test_safety_spec_airbag_count(self):
        spec = SafetySpecification(
            variant=self.variant,
            airbag=7,
            abs=True,
            vsc=True,
        )
        self.assertEqual(spec.airbag,7)
        self.assertTrue(spec.abs)
        self.assertTrue(spec.vsc)
            
    def test_safety_spec_boolean_default_false(self):
        spec = SafetySpecification(variant=self.variant)
        bool_fields = [
            "pcs", "lda", "lta", "drcc", "ahb", "bsm", "rcta",
            "abs", "ba", "ebd", "vsc", "trc", "hac", "ebs", "tpws",
        ]
        for field in bool_fields:
            self.assertFalse(getattr(spec, field), f"{field} should default to False")
        