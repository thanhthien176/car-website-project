from decimal import Decimal
from unittest.mock import MagicMock
from urllib import request
from django.test import TestCase

from cars.templatetags.car_filters import million_vnd, star_range, active_url

class MillionVndFilterTest(TestCase):
    
    def test_normal_value(self):
        self.assertEqual(million_vnd(Decimal("1_000_000")), "1 triệu đồng")
        
    def test_none_returns_lien_he(self):
        self.assertEqual(million_vnd(None), "Liên hệ")
        
    def test_zero_returns_lien_he(self):
        self.assertEqual(million_vnd(0), "Liên hệ")
        
    def test_invalid_value_return_str(self):
        self.assertEqual(million_vnd("abc"), "abc")
        
class StarRangeFilterTest(TestCase):
    
    def test_full_stars(self):
        result = star_range(5.0)
        self.assertEqual(result, ["bi-star-fill"]*5)
        
    def test_half_star(self):
        result = star_range(3.5)
        self.assertEqual(result[0], "bi-star-fill")
        self.assertEqual(result[1], "bi-star-fill")
        self.assertEqual(result[2], "bi-star-fill")
        self.assertEqual(result[3], "bi-star-half")
        self.assertEqual(result[4], "bi-star")
        
    def test_zero_rating(self):
        result = star_range(0)
        self.assertEqual(result, ["bi-star"]*5)
        
    def test_invalid_string_returns_empty(self):
        result = star_range("abc")
        self.assertEqual(result, [])
        
    def test_none_returns_empty(self):
        result = star_range(None)
        self.assertEqual(result, [])
        
class ActiveUrlTagTest(TestCase):
    
    def test_returns_empty_when_no_requests_in_context(self):
        result = active_url({}, "home")
        self.assertEqual(result, "")
        
    def test_returns_empty_when_request_has_no_resolver_match(self):
        request = MagicMock()
        request.resolver_match = None
        result = active_url({'request': request}, "home")
        self.assertEqual(result, "")
        
    def test_returns_active_when_url_name_matches(self):
        request = MagicMock()
        request.resolver_match.url_name = "home"
        result = active_url({'request': request}, "home")
        self.assertEqual(result, "active")
        
    def test_returns_empty_when_url_name_differs(self):
        request = MagicMock()
        request.resolver_match.url_name = "brand_list"
        result = active_url({'request': request}, "home")
        self.assertEqual(result, "")
        
    def test_returns_active_when_view_name_matches(self):
        request = MagicMock()
        request.resolver_match.view_name = "cars:home"
        result = active_url({'request': request}, "cars:home")
        self.assertEqual(result, "active")
        
    def test_returns_empty_when_view_name_differs(self):
        request = MagicMock()
        request.resolver_match.view_name = "cars:detail"
        result = active_url({'request': request}, "blog:detail")
        self.assertEqual(result, "")
        
    def test_url_name_and_view_name_both_checked(self):
        request = MagicMock()
        request.resolver_match.view_name = "cars:list"
        request.resolver_match.url_name = "list"
        result = active_url({'request': request}, "cars:list")
        self.assertEqual(result, "active")
        
        