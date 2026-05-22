from unittest.mock import MagicMock
from django.test import TestCase

from cars.utils.upload_utils import UploadToPath

class UpLoadToPathTest(TestCase):
    
    def _make_instance(self, slug_val:str, related_slug:str | None=None):
        instance = MagicMock()
        instance.slug = slug_val
        
        if related_slug is not None:
            instance.car = MagicMock()
            instance.car.slug = related_slug
            
        return instance
    
    def test_basic_path_format(self):
        uploader = UploadToPath("brand", "logos")
        instance = self._make_instance("toyota")
        path = uploader(instance, "logo.jpg")
        # brand/logos/<slug>-<8hex>.jpg
        self.assertTrue(path.startswith("brand/logos/toyota-"))
        self.assertTrue(path.endswith(".jpg"))
        
    def test_path_without_subpath(self):
        uploader = UploadToPath("brand")
        instance = self._make_instance("kia")
        path = uploader(instance, "logo.png")
        self.assertTrue(path.startswith("brand/kia-"))
        self.assertNotIn("//", path)
        
    def test_nested_slug_field(self):
        uploader = UploadToPath("cars", "gallery", slug_field="car.slug")
        instance = self._make_instance("ignored", related_slug="toyota-camry")
        path = uploader(instance, "photo.webp")
        self.assertIn("toyota-camry", path)
        self.assertTrue(path.startswith("cars/gallery"))
        
    # ── Slug truncation ──────────────────────────────────────────────────
    def test_slug_truncated_to_60_chars(self):
        long_slug = "a"*100
        uploader = UploadToPath("cars", "gallery")
        instance = self._make_instance(long_slug)
        path = uploader(instance, "img.jpg")
        filename = path.split("/")[-1]
        # filename = slug[:60]-<8hex>.jpg → slug part is 60 characters
        # rsplit("-",1): split from right to left, only split one time
        slug_part = filename.rsplit("-", 1)[0]
        self.assertEqual(len(slug_part), 60)
        
    def test_empty_slug_uses_uuid_only(self):
        uploader = UploadToPath("cars", "gallery")
        instance = self._make_instance("")
        path = uploader(instance, "img.webp")
        filename = path.split("/")[-1]
        # Only <8hex>.webp - don't have "-" char before uuid
        self.assertFalse(filename.startswith("-"))
    
    # ── UUID uniqueness ──────────────────────────────────────────────────
    def test_two_calls_produce_different_paths(self):
        uploader = UploadToPath("cars", "gallery")
        instance = self._make_instance("toyota")
        path1 = uploader(instance, "logo.png")
        path2 = uploader(instance, "logo.png")
        self.assertNotEqual(path1, path2)
    
     # ── Extension preserved ──────────────────────────────────────────────
    def test_extension_lowercased(self):
        uploader = UploadToPath("cars", "gallery")
        instance = self._make_instance("toyota")
        path = uploader(instance, "CARS.PNG")
        self.assertTrue(path.endswith(".png"))
        
    # ── Equality ─────────────────────────────────────────────────────────
    def test_equal_instances(self):
        a = UploadToPath("cars", "gallery", "slug")
        b = UploadToPath("cars", "gallery", "slug")
        self.assertEqual(a, b)
    
    def test_unequal_instances(self):
        a = UploadToPath("brand", "logos")
        b = UploadToPath("cars", "gallery")
        self.assertNotEqual(a, b)
        
        