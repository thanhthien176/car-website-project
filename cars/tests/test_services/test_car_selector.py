from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from cars.services.car_selector import CarSelector
from cars.tests.helpers.helper_models import make_brand, make_variant, make_car_model
from cars.models import Review, CarModel, BodyType


class CarSelectorQueryTest(TestCase):
    
    def setUp(self) -> None:
        self.selector = CarSelector()
        self.brand = make_brand(name='Toyota')
        self.model = make_car_model(brand=self.brand, name='Camry')
        self.variant = make_variant(
            car_model=self.model,
            name='2.5Q',
            price_min=Decimal("1_100_000_000"),
            price_max=Decimal("1_200_000_000")
        )
    
    def test_get_featured_brand_returns_active_only(self):
        inactive = make_brand(name='inactive', is_active=False)
        result = list(self.selector.get_featured_brands())
        names = [b.name for b in result]
        self.assertIn('Toyota', names)
        self.assertNotIn('inactive', names)
        
    def test_get_featured_brands_has_model_count(self):
        result = list(self.selector.get_featured_brands())
        brand = next(b for b in result if b.name=="Toyota")
        self.assertEqual(brand.model_count, 1)
        
    def test_get_lastest_variants_return_active_only(self):
        inactive = make_variant(
            car_model= self.model,
            name='Old',
            is_active=False,
        )
        result = list(self.selector.get_latest_variants(AnonymousUser()))
        slugs = [v.slug for v in result]
        self.assertIn(self.variant.slug, slugs)
        self.assertNotIn(inactive.slug, slugs)
    
    def test_get_top_rated_models_excludes_zero_rating(self):
        result = list(self.selector.get_top_rated_models())
        self.assertEqual(result, [])
        
    def test_get_top_rated_models_returns_when_has_rating(self):
        Review.objects.create(
            car=self.model,
            author_name="Tester",
            rating=5,
            title="Great",
            content="Good car",
            is_approved=True,
        )
        self.model.refresh_from_db()
        result = list(self.selector.get_top_rated_models())
        self.assertEqual(result[0].pk, self.model.pk)
        self.assertEqual(len(result), 1)
        

        
class CarSelectorSearchTest(TestCase):
    def setUp(self) -> None:
        self.selector = CarSelector()
        self.toyota = make_brand(name="Toyota")
        self.camry = make_car_model(brand=self.toyota, name='Camry')
        self.vios = make_car_model(brand=self.toyota, name='Vios')
        self.honda = make_brand(name="Honda")
        self.city = make_car_model(brand=self.honda, name='City')
        
    def test_empty_query_returns_all(self):
        result = list(self.selector.search_car_models(""))
        self.assertIn(self.camry, result)
        self.assertIn(self.city, result)
        
        
    def test_none_query_returns_all(self):
        result = list(self.selector.search_car_models(None))
        self.assertIn(self.camry, result)
        self.assertIn(self.city, result)
        
    def test_match_by_model_name(self):
        result = list(self.selector.search_car_models("Camry"))
        self.assertIn(self.camry, result)
        self.assertNotIn(self.city, result)
        self.assertNotIn(self.vios, result)
        
    def test_match_by_brand_name(self):
        result = list(self.selector.search_car_models("Toyota"))
        self.assertIn(self.camry, result)
        self.assertIn(self.vios, result)
        self.assertNotIn(self.city, result)
        
    def test_no_match_returns_empty(self):
        result = list(self.selector.search_car_models("Civic"))
        self.assertEqual(result, [])
        
    def test_custom_qs_is_used_as_base(self):
        base_qs = CarModel.objects.filter(pk=self.camry.pk)
        result = list(self.selector.search_car_models("Camry", qs=base_qs))
        self.assertEqual(len(result), 1)
        
        
class CarSelectorFilterTest(TestCase):
    def setUp(self) -> None:
        self.selector = CarSelector()
        self.toyota = make_brand(name="Toyota")
        self.camry = make_car_model(brand=self.toyota, name='Camry')
        self.vios = make_car_model(brand=self.toyota, name='Vios')
        self.honda = make_brand(name="Honda")
        self.crv = make_car_model(brand=self.honda, name='crv')
        self.camry_v1 = make_variant(
            car_model=self.camry,
            name="HEV",
            fuel_type="hybrid",
            price_min=Decimal("1_000_000_000"),
            price_max=Decimal("1_100_000_000"),
        )
        self.vios_v1 = make_variant(
            car_model=self.vios,
            name="1.6G",
            fuel_type="gasoline",
            price_min=Decimal("500_000_000"),
            price_max=Decimal("550_000_000"),
        )
        self.crv_v1 = make_variant(
            car_model=self.crv,
            name="1.6G",
            fuel_type="gasoline",
            price_min=Decimal("530_000_000"),
            price_max=Decimal("580_000_000"),
        )
    
    def _base_qs(self):
        return CarModel.objects.all()
    
    def test_filter_by_brand_slug(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {'brand': 'honda'}
        ))
        self.assertIn(self.crv, result)
        self.assertNotIn(self.vios, result)
        
    def test_filter_by_brand_slug_no_match(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {'brand': 'Vinfast'}
        ))
        self.assertNotIn(self.crv, result)
        self.assertNotIn(self.vios, result)
        
    def test_filter_by_fuel_type(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {'fuel': 'gasoline'}
        ))
        self.assertIn(self.vios, result)
        self.assertIn(self.crv, result)
        self.assertNotIn(self.camry, result)
        
    def test_filter_by_min_price(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {"min_price": "700"}
        ))
        self.assertIn(self.camry, result)
        self.assertNotIn(self.vios, result)
        
    def test_filter_by_max_price(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {'max_price': "600"}
        ))
        self.assertIn(self.crv, result)
        self.assertNotIn(self.camry, result)
        
    def test_empty_params_returns_all(self):
        result = list(self.selector.apply_filters(self._base_qs(), {}))
        self.assertIn(self.crv, result)
        self.assertIn(self.vios, result)
        self.assertIn(self.camry, result)
        
    def test_filter_by_body_slug(self):
        sedan = BodyType.objects.create(name="Sedan", slug="sedan")
        suv = BodyType.objects.create(name="SUV", slug="suv")
        self.camry.body_type = sedan
        self.vios.body_type = sedan
        self.crv.body_type = suv
        self.camry.save()
        self.vios.save()
        self.crv.save()
        
        result = list(self.selector.apply_filters(
            self._base_qs(), {'body': "sedan"}
        ))
        self.assertIn(self.camry, result)
        self.assertIn(self.vios, result)
        self.assertNotIn(self.crv, result)
        
    def test_filter_invalid_price_string_ignored(self):
        result = list(self.selector.apply_filters(
            self._base_qs(), {'min_price': 'abc', 'max_price': 'xyz'}
        ))
        self.assertIn(self.camry, result)
        self.assertIn(self.vios, result)
        self.assertIn(self.crv, result)
        
    
        
        

    
    