from django.test import TestCase

from cars.tests.helpers.helper_models import make_car_model, make_brand
from cars.models import Review

class AvgRatingSignalTest(TestCase):
    """
    Check post_delete/post_save signal of Review
    and ensure the avg_rating on CarModel is correctly updated.
    """
    def setUp(self):
        self.brand = make_brand(name="Honda")
        self.car_model = make_car_model(brand=self.brand, name="Civic")
        
    def _make_review(self, rating, is_approved=True):
        return Review.objects.create(
            car = self.car_model,
            author_name="Tester",
            rating=rating,
            title="Test",
            content="Test content",
            is_approved=is_approved,
        )
        
    def test_avg_rating_updated_on_review_created(self):
        self._make_review(4)
        self._make_review(5)
        self.car_model.refresh_from_db()
        self.assertAlmostEqual(float(self.car_model.avg_rating), 4.5)
        
    def test_unapproved_reviews_excluded_from_avg(self):
        self._make_review(4, is_approved=True)
        self._make_review(5, is_approved=False)
        self.car_model.refresh_from_db()
        self.assertAlmostEqual(float(self.car_model.avg_rating), 4)
        
    def test_avg_rating_zero_when_no_approved_reviews(self):
        self._make_review(4, is_approved=False)
        self.car_model.refresh_from_db()
        self.assertEqual(self.car_model.avg_rating, 0)
        
    def test_avg_rating_updated_on_review_delete(self):
        r1 = self._make_review(4)
        r2 = self._make_review(3)
        self.car_model.refresh_from_db()
        self.assertAlmostEqual(float(self.car_model.avg_rating), 3.5)
        
        r2.delete()
        self.car_model.refresh_from_db()
        self.assertEqual(self.car_model.avg_rating, 4)
        
    def test_avg_rating_zero_when_all_reviews_deleted(self):
        r =self._make_review(5)
        self.car_model.refresh_from_db()
        self.assertAlmostEqual(float(self.car_model.avg_rating), 5.0)
        r.delete()
        self.assertAlmostEqual(self.car_model.avg_rating, 0)
        
        
        