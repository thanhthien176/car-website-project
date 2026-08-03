from typing import TYPE_CHECKING, Protocol
from django.db import models

if TYPE_CHECKING:
    class ModelWithMetaProtocol(Protocol):
        _meta: models.Model

class SpecificationDisplayMixin(models.Model):
    """Mixin for models *Specification*: automatically generate a list of fields to use
    Render to template, no need to hard code field names."""
    class Meta:
        abstract = True
        
    _display_exclude = {'id', 'variant'}
    
    def get_display_items(self):
        items = []
        for field in self._meta.get_fields():
            if not isinstance(field, models.Field):
                continue
            if field.name in self._display_exclude or field.is_relation:
                continue
            
            value = getattr(self, field.name)
            
            if isinstance(field, models.BooleanField):
                if not value:
                    continue
                display_value = True
            else:
                if value in ['', None]:
                    continue
                display_value = value
                
            items.append({
                'field_name': field.name,
                'label': field.help_text or field.verbose_name.capitalize(),
                'value': display_value,
                'is_boolean': isinstance(field, models.BooleanField)
            })
        return items
    
    @property
    def has_data(self):
        """Decides whether the tab should appear or not."""
        return bool(self.get_display_items())