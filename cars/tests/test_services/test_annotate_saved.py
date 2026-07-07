from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from cars.models import CarVariant
from cars.tests.helpers import make_variant, make_car_model
from users.tests.helpers import make_saved_car, make_user

class AnnotateSavedTest(TestCase):
    def setUp(self):
        self.car_model = make_car_model()
        self.v1 = make_variant(car_model=self.car_model, name="2.0G")
        self.v2 = make_variant(car_model=self.car_model, name="2.0HEV")
        self.user = make_user(username="saved")
        
        
     # ── Anonymous branch ─────────────────────────────────────────────────
    def test_anonymous_user_all_false(self):
        make_saved_car(user=self.user, car=self.v1)
        
        qs = CarVariant.objects.filter(is_active=True).annotate_saved(AnonymousUser())
        results = {v.pk: v.is_saved for v in qs}
        
        self.assertFalse(results[self.v1.pk])
        self.assertFalse(results[self.v2.pk])
        
    def test_anonymous_branch_uses_no_extra_query(self):
        with self.assertNumQueries(1):
            list(CarVariant.objects.all().annotate_saved(AnonymousUser()))
            
    # ── Authenticated branch ─────────────────────────────────────────────
    def test_saved_variant_is_true(self):
        make_saved_car(user=self.user, car=self.v1)
        
        qs = CarVariant.objects.all().annotate_saved(self.user)
        
        results = {v.pk: v.is_saved for v in qs}
        
        self.assertTrue(results[self.v1.pk])
        self.assertFalse(results[self.v2.pk])
        
        
    def test_only_current_user_saved_state_counted(self):
        other_user = make_user(username="other_user")
        make_saved_car(user=other_user, car=self.v2)
        
        qs = CarVariant.objects.all().annotate_saved(self.user)
        results = {v.pk: v.is_saved for v in qs}
        
        self.assertFalse(results[self.v1.pk])
        self.assertFalse(results[self.v2.pk])
        
    def test_no_n_plus_one_regardless_of_row_count(self):
        for i in range(5):
            make_variant(car_model=self.car_model, variant_name=f"trim-{i}")
            
        with self.assertNumQueries(1):
            qs = CarVariant.objects.all().annotate_saved(self.user)
            list(qs)
        
    def test_deleted_saved_car_reflected_as_false(self):
        saved = make_saved_car(user=self.user, car=self.v1)
        saved.delete()
        
        qs = CarVariant.objects.all().annotate_saved(self.user)
        results = {v.pk: v.is_saved for v in qs}
        
        self.assertFalse(results[self.v1.pk])
        
        
        
        