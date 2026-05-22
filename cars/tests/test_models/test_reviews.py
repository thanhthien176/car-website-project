from django.test import TestCase

from cars.models import Review
from helpers.helper_models import make_car_model

class ReviewTest(TestCase):
    def setUp(self) -> None:
        self.car_model = make_car_model()
        
    def _make_review(self, rating=5, is_approved=True, **kwargs):
        defaults = dict(
            car=self.car_model,
            author_name = "Nguyen Van A",
            rating=rating,
            title=f"{self.car_model.name} so good",
            content="Chạy êm, tiết kiệm xăng, bền bỉ",
            is_approved=is_approved,            
        )
        defaults.update(kwargs)
        return Review.objects.create(**defaults)
    
    def test_str(self):
        review = self._make_review(rating=4)
        self.assertIn("Nguyen Van A", str(review))
        self.assertIn("4", str(review))
        
    def test_default_ordering_newest_first(self):
        r1 = self._make_review(title="first")
        r2 = self._make_review(title="second")
        reviews = list(Review.objects.filter(car=self.car_model))
        self.assertEqual(reviews[0], r2)
        
    def test_rating_choices_valid(self):
        valid_ratings = [1, 2, 3, 4, 5]
        for rating in valid_ratings:
            r = self._make_review(rating=rating)
            self.assertEqual(r.rating, rating)
        
    
    