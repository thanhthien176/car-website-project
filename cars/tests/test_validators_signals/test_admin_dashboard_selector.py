import json
from django.test import TestCase

from helpers.helper_models import make_brand, make_car_model, make_variant
from cars.models import Review
from cars.services.dashboard import AdminDashboardSelector

class AdminDashboardSelectorTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand(name="Honda")
        self.car_model = make_car_model(brand=self.brand, name="Civic")
        self.v1 = make_variant(
            car_model=self.car_model,
            variant_name="RS",
            fuel_type="gasoline",
            price_min=889_000_000,
            price_max=897_000_000,
        )
        self.v2 = make_variant(
            car_model=self.car_model,
            variant_name="G",
            fuel_type="gasoline",
            price_min=789_000_000,
            price_max=797_000_000,
        )
        review1 = Review.objects.create(
            car=self.car_model, author_name="A", rating=5,
            title="Good", content="Good", is_approved=True,
        )
        review1 = Review.objects.create(
            car=self.car_model, author_name="B", rating=4,
            title="OK", content="OK", is_approved=True,
        )
        
    
    def _selector(self):
        return AdminDashboardSelector()
    
    def test_get_kpi_card_counts(self):
        kpis = self._selector().get_kpi_card()
        self.assertEqual(kpis['total_brands'], 1)
        self.assertEqual(kpis['total_variants'], 2)
        self.assertEqual(kpis['total_reviews'], 2)
        
    
    def test_get_review_stats_avg(self):
        stats = self._selector().get_review_stats()
        self.assertAlmostEqual(float(stats['avg_rating_global']), 4.5)        
    
    def test_get_review_stats_rating_dist_has_5_stars(self):
        stats = self._selector().get_review_stats()
        dist = {item['star']: item['count'] for item in stats['rating_dist']}
        self.assertEqual(dist[5], 1)
        self.assertEqual(dist[4], 1)
        self.assertEqual(dist[3], 0)    


    def test_get_fuel_type_data_returns_json(self):
        labels_json, data_json = self._selector().get_fuel_type_data()
        labels = json.loads(labels_json)
        data = json.loads(data_json)
        self.assertIsInstance(labels, list)
        self.assertIsInstance(data, list)
        self.assertEqual(len(labels), len(data))
    
    def test_get_price_bracket_chart_data(self):
        labels_json, data_json = self._selector().get_price_bracket_chart_data()
        labels = json.loads(labels_json)
        data = json.loads(data_json)
        self.assertEqual(len(labels), 4)
        total = sum(data)
        self.assertEqual(total, 2)
    
    def test_get_price_overview_keys(self):
        overview = self._selector().get_price_overview()
        self.assertEqual(overview["min"], 789)
        self.assertEqual(overview["max"], 897)
        self.assertEqual(overview['avg_min'], 839)
    
    
    def test_get_full_context_contains_required_keys(self):
        ctx = self._selector().get_full_context()
        required_keys = [
            "total_brands", "total_variants", "avg_rating_global",
            "fuel_chart_labels", "body_chart_labels", "price_bracket_labels",
            "completeness", "price_overview",
        ]
        for key in required_keys:
            self.assertIn(key, ctx, f"Missing {key}")
        
    def test_get_data_completeness_zero_variants(self):
        result = self._selector().get_data_completeness(0)
        self.assertEqual(result, [])
    
    def test_get_data_completeness_pct_in_range(self):
        result = self._selector().get_data_completeness(2)
        for item in result:
            self.assertGreaterEqual(item['pct'], 0)
            self.assertLessEqual(item['pct'], 100)