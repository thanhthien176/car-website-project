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
    
    
    @classmethod
    def get_comparison_tabs(cls, variants):
        """
        Build tabs so sánh cho N variants.
        Field xuất hiện nếu >=1 variant "có nghĩa" với field đó
        (theo đúng định nghĩa has_data/get_display_items của mixin).
        Field ẩn nếu tất cả variant đều rỗng/False/None.
        """
        tabs = []
        for accessor, model in cls.get_spec_relations():
            instances = [cls._safe_get(v, accessor) for v in variants]

            if not any(inst and inst.has_data for inst in instances):
                continue  # không xe nào có data cho spec model này -> bỏ tab

            # Gom field "có nghĩa" từ TẤT CẢ variant (giữ thứ tự xuất hiện đầu tiên)
            meaningful = {}
            for inst in instances:
                if inst is None:
                    continue
                for item in inst.get_display_items():
                    meaningful.setdefault(item['field_name'], {
                        'label': item['label'],
                        'is_boolean': item['is_boolean'],
                    })

            if not meaningful:
                continue

            rows = []
            for field_name, meta in meaningful.items():
                values = [
                    getattr(inst, field_name) if inst is not None else None
                    for inst in instances
                ]
                rows.append({
                    'field': field_name,
                    'label': meta['label'],
                    'is_boolean': meta['is_boolean'],
                    'values': values,  # cùng thứ tự với `variants`
                })

            tabs.append({
                'key': accessor,
                'label': model._meta.verbose_name,
                'rows': rows,
            })

        return tabs
    
    @staticmethod
    def _safe_get(variant, accessor):
        try:
            return getattr(variant, accessor)
        except ObjectDoesNotExist:
            return None