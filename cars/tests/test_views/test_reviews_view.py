from urllib import response

from django.test import TestCase
from django.urls import reverse

from cars.models import Review
from cars.tests.helpers.helper_models import make_brand, make_car_model

class ReviewSubmitViewTest(TestCase):
    def setUp(self) -> None:
        self.brand = make_brand(name='Toyota')
        self.car_model = make_car_model(brand=self.brand, name='Innova')
        self.url = reverse('cars:review_submit', kwargs={'slug': self.car_model.slug})
        
    def test_get_returns_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        
    def test_post_valid_data_creates_review(self):
        data = {
            'author_name': 'Nguyen Van A',
            'rating': 5,
            'title': 'Xe rat tot',
            'content': 'Chay em, tiet kiem xang',
            'pros': 'Tot',
            'cons': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.author_name, 'Nguyen Van A')
        
    def test_post_forces_is_approved_false(self):
        data = {
            'author_name': 'Nguyen Van A',
            'rating': 5,
            'title': 'Xe rat tot',
            'content': 'Chay em',
            'pros': '',
            'cons': '',
            'is_approved': True,
        }
        
        self.client.post(self.url, data)
        review = Review.objects.first()
        self.assertFalse(review.is_approved)
        
    def test_post_invalid_data_does_not_create_review(self):
        data = {
            'author_name': '',  # required field rỗng
            'rating': 5,
            'title': 'Xe rat tot',
            'content': 'Chay em',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.count(), 0)
        
    def test_post_redirects_on_success(self):
        data = {
            'author_name': 'A',
            'rating': 4,
            'title': 'OK',
            'content': 'OK',
            'pros': '',
            'cons': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)