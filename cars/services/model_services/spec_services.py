from functools import lru_cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.reverse_related import OneToOneRel


class SpecService:
    
    @classmethod
    # @lru_cache(maxsize=1)
    def get_spec_relations(cls):
        """
        Returns [(accessor_name, related_model), ...] for EVERY OneToOneField
        point to CarVariant (Dimension, Engine, Safety, ...).
        Add new model spec -> automatically appears here, no further changes.
        """
        from cars.models import CarVariant, SpecificationDisplayMixin
        
        relations = []
        for field in CarVariant._meta.get_fields():
            if isinstance(field, OneToOneRel):
                if isinstance(field.related_model, type) and issubclass(field.related_model, SpecificationDisplayMixin):
                    relations.append((field.get_accessor_name(), field.related_model))
                
        return relations

    @classmethod
    def variant_queryset_with_specs(cls):
        from cars.models import CarVariant
        accessors = [name for name, _ in cls.get_spec_relations()]
        return CarVariant.objects.select_related(*accessors)

    @classmethod
    def get_spec_tabs(cls, variant):
        tabs = []
        for accessor, model in cls.get_spec_relations():
            try:
                instance = getattr(variant, accessor)
            except ObjectDoesNotExist:
                continue
            if instance and instance.has_data:
                tabs.append({
                    'key': accessor,
                    'label': model._meta.verbose_name,
                    'items': instance.get_display_items(),
                })

        return tabs