import io
import pytest
from PIL import Image, UnidentifiedImageError
from unittest.mock import MagicMock, patch, Mock

from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from cars.utils.image_utils import (
    convert_to_webp,
    _image_to_webp,
    image_byte_to_webp,
    download_image, 
    download_and_convert_webp,
    save_remote_image_to_field)

class ConvertToWebpTest(TestCase):
    """
    Testing conversion logic without a real image file —
    using PIL to create an in-memory image.
    """
    def _create_test_image(self, width=200, height=150, mode="RGB"):
        color = (
            (100, 150, 200, 128)
            if mode == "RGBA"
            else (100, 150, 200)
        )
        
        img = Image.new(mode, (width, height), color=color)
        buf = io.BytesIO()
        fmt = "PNG" if mode == "RGBA" else "JPEG"
        img.save(buf, format=fmt)
        
        return SimpleUploadedFile(
            name=f"test_image.{fmt.lower()}",
            content=buf.getvalue(),
            content_type=f"image/{fmt.lower()}"
        )

    
    def test_returns_content_file_for_valid_image(self):
        field = self._create_test_image(mode="RGB")
        
        result = convert_to_webp(field)
        
        self.assertIsNotNone(result)
        
        self.assertEqual(Image.open(result).format, "WEBP")
        self.assertTrue(result.name.endswith(".webp"))
        
    def test_return_none_for_empty_field(self):
        self.assertIsNone(convert_to_webp(None))
        
    def test_returns_none_on_open_error(self):
        field = self._create_test_image()
        
        with patch("cars.utils.image_utils.Image.open", side_effect=UnidentifiedImageError):
            result = convert_to_webp(field)
            
            self.assertIsNone(result)
        
    def test_rgba_image_handled(self):
        field = self._create_test_image(mode="RGBA")
        
        result = convert_to_webp(field)
        
        self.assertIsNotNone(result)
    
        img = Image.open(result)
        self.assertEqual(img.format, "WEBP")
        self.assertEqual(img.mode, "RGBA")
        
    def test_max_size_resize_image(self):
        field = self._create_test_image(width=3000, height=2000)
        result = convert_to_webp(field, quality=85, max_size=(1280, 1280))
        
        self.assertIsNotNone(result)
    
        img = Image.open(result)
        self.assertLessEqual(img.size[0], 1280)
        self.assertLessEqual(img.size[1], 1280)
    
    def test_file_extension_is_changed_to_webp(self):
        field = self._create_test_image()
        field.name = "toyota-abc123.jpg"
        
        result = convert_to_webp(field)
        
        print(f"DEBUG: result.name sau khi chạy: {result.name}")
        self.assertTrue(result.name.endswith(".webp"))
        
    @patch("PIL.Image.Image.save")
    def test_image_to_webp_return_none_when_save_fail(self, mock_save):
        mock_save.side_effect = Exception("encode error")
        
        img = Image.new("RGB", (100,100))
        
        result = _image_to_webp(img)
        
        self.assertIsNone(result)
        
    def test_image_byte_to_webp_success(self):
        image_bytes = self._create_test_image().read()
        
        result = image_byte_to_webp(image_bytes)
        
        self.assertIsNotNone(result)
        self.assertTrue(result.name.endswith(".webp"))
        
    def test_image_bytes_to_webp_invalid_bytes(self):
        result = image_byte_to_webp(b"invalid image")
        self.assertIsNone(result)
        
    @patch("cars.utils.image_utils.requests.get")
    def test_download_image_success(self, mock_get):
        response = Mock()
        response.content = b"image-data"
        response.raise_for_status.return_value = None
        
        mock_get.return_value = response
        
        result = download_image("https://example.com/car.jpg")
        
        assert result == b"image-data"
        
    @patch("cars.utils.image_utils.requests.get")
    def test_download_image_fail(self, mock_get):
        mock_get.side_effect = Exception("network error")
        
        result = download_image("https://example.com/car.jpg")
        
        self.assertIsNone(result)
        
    @patch("cars.utils.image_utils.download_image")
    def test_download_and_convert_returns_none_when_download_fail(self, mock_download):
        mock_download.return_value = None
        
        result = download_and_convert_webp("https://example.com/car.jpg")
        
        self.assertIsNone(result)
        
    @patch("cars.utils.image_utils.download_image")
    def test_download_and_convert_success(self, mock_download):
        mock_download.return_value = self._create_test_image().read()
        
        result = download_and_convert_webp("https://example.com/car.jpg")
        self.assertIsNotNone(result)
        
    
    @patch("cars.utils.image_utils.download_and_convert_webp")
    def test_save_remote_image_success(self, mock_convert):
        webp = ContentFile(
            b"abc",
            name="test.webp"
        )
        mock_convert.return_value = webp
        
        field = Mock()
        
        instance = Mock()
        instance.logo = field
        
        result = save_remote_image_to_field(
            instance,
            "logo",
            "https://example.com/logo.png"
        )
        
        self.assertTrue(result)
        
        field.save.assert_called_once_with(
            "test.webp",
            webp,
            save=False,
        )
        
    @patch("cars.utils.image_utils.download_and_convert_webp")
    def test_save_remote_image_return_false_when_convert_fail(self, mock_convert):
        mock_convert.return_value = None
        result = save_remote_image_to_field(
            MagicMock(),
            "logo",
            "url"
        )
        self.assertFalse(result)
        
    @patch("cars.utils.image_utils.download_and_convert_webp")
    def test_save_remote_image_raise_value_error(self, mock_convert):
        mock_convert.return_value = ContentFile(
            b"abc",
            name="test.webp"
        )
        
        class Dummy:
            pass
        
        with pytest.raises(ValueError):
            save_remote_image_to_field(
                Dummy(),
                "logo",
                "url",
            )
    
        
    
    
            
        
        
    