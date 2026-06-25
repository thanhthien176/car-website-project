from django.test import TestCase
from django.core.exceptions import ValidationError

from cars.validators import validate_image_extension
from cars.tests.helpers.helper_images import mock_image

class ValidateImageExtensionTest(TestCase):
    
    def test_jpg_allowed(self):
        validate_image_extension(mock_image("photo.jpg", 1024))
        
    def test_jpeg_allowed(self):
        validate_image_extension(mock_image("photo.jpeg", 1024))
        
    def test_png_allowed(self):
        validate_image_extension(mock_image("photo.png", 1024))
        
    def test_webp_allowed(self):
        validate_image_extension(mock_image("photo.webp", 1024))
        
    def test_uppercase_extension_allowed(self):
        validate_image_extension(mock_image("photo.JPG", 1024))
        
    def test_gif_rejected(self):
        with self.assertRaises(ValidationError):
            validate_image_extension(mock_image("photo.gif", 1024))
            
    def test_svg_rejected(self):
        with self.assertRaises(ValidationError):
            validate_image_extension(mock_image("photo.svg", 100))
            
    def test_exe_rejected(self):
        with self.assertRaises(ValidationError):
            validate_image_extension(mock_image("malware.exe", 100))
        
    def test_no_extension_rejected(self):
        with self.assertRaises(ValidationError):
            validate_image_extension(mock_image("empty", 100))
    
    def test_error_message_contains_extension(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_image_extension(mock_image("car.bmp", 100))
        
        self.assertIn("bmp", str(ctx.exception))
        

  