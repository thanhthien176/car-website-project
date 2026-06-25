from django.test import TestCase
from django.core.exceptions import ValidationError

from cars.validators import validate_image_size
from cars.tests.helpers.helper_images import mock_image


class ValidateImageSizeTest(TestCase):
    LIMIT = 5 * 1024 * 1024
    
    def test_exactly_at_limit_passes(self):
        img = mock_image(name="photo.jpg", size_bytes=self.LIMIT)
        validate_image_size(img)
    
    def test_under_limit_passes(self):
        img = mock_image("photo.jpg", size_bytes=self.LIMIT-1)
        validate_image_size(img)
        
    def test_over_limit_raises(self):
        img = mock_image("photo.jpg", self.LIMIT+1)
        with self.assertRaises(ValidationError) as ctx:
            validate_image_size(img)
        self.assertIn("5", str(ctx.exception))
        
    def test_zero_size_passes(self):
        img = mock_image("empty.jpg", 0)
        validate_image_size(img)    