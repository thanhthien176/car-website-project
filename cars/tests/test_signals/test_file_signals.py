from unittest.mock import MagicMock, patch

from django.db.models.signals import pre_save
from django.test import TestCase

from cars.models import Brand
from cars.signals import _delete_old_file_on_change
from cars.tests.helpers.helper_models import make_brand

class DeleteBrandLogoSignalTest(TestCase):
    """Tests delete_image_file signal."""
    
    def test_delete_brand_calls_delete_image_helper(self):
        brand = make_brand(name="Toyota")
        
        mock_file = MagicMock()
        mock_file.name = "brand/logos/toyota-abc.webp"
        mock_file.storage.exists.return_value = True
        brand.logo = mock_file
        
        with patch("cars.signals._delete_image_field") as mock_delete:
            brand.delete()
            mock_delete.assert_called_once_with(brand)
            
    def test_delete_brand_without_no_error(self):
        brand = make_brand(name="Kia")
        brand.delete()
        
class AutoDeleteLogoOnChangeTest(TestCase):
    """Test auto_delete_logo_on_change signal."""
    
    def test_delete_old_file_on_change(self):
        brand = make_brand(name="Toyota")
        
        with patch("cars.signals._delete_old_file_on_change") as mock_helper:
            
            pre_save.send(
                sender=Brand,
                instance=brand,
            )
        mock_helper.assert_called_once_with(
            brand,
            "logo"
        )
    
    def test_old_logo_deleted_when_logo_changed(self):
        brand = make_brand(name='Honda')
        
        old_logo = MagicMock()
        old_logo.name = "brand/logos/old.webp"
        
        
        new_logo = MagicMock()
        new_logo.name = "brand/logos/new.webp"
        
        with patch.object(
            Brand.objects,
            "get",
            return_value=MagicMock(logo=old_logo)
        ):
            brand.logo = new_logo
            
            _delete_old_file_on_change(
                brand,
                "logo",
            )
            
        old_logo.delete.assert_called_once_with(save=False)
        
        
    def test_old_logo_not_deleted_when_logo_unchanged(self):
        brand = make_brand(name="Mazda")
        
        same_logo = MagicMock()
        same_logo.name = "brand/logos/same.webp"
        
        with patch.object(
            Brand.objects,
            "get",
            return_value=MagicMock(logo=same_logo)
        ):
            brand.logo = same_logo
            
            _delete_old_file_on_change(
                brand,
                "logo",
            )
        
        same_logo.delete.assert_not_called()
        
    def test_new_brand_skips_signal(self):
        brand = Brand(name="NewBrand", country_of_origin="Japan")
        
        with patch.object(Brand.objects, "get") as mock_get:
            _delete_old_file_on_change(brand, "logo")
        
        mock_get.assert_not_called()