from blogs.models import CarDescription

def get_description_for_variant(variant):
    """
    Resolve which CarDescription to display for a given CarVariant.
 
    Priority:
        1. A primary description written specifically for this variant
           (variant=<this variant>, is_primary=True).
        2. A primary description shared across the whole car_model line
           (variant=None, is_primary=True) — used when no variant-specific
           override exists, avoiding duplicated near-identical text across
           sibling variants (e.g. 2.0G, 2.5HEV).
        3. None — caller decides how to render an empty state.
    """
    variant_specific = (
        CarDescription.objects
        .filter(variant=variant, is_primary=True, is_published=True)
        .prefetch_related("sections")
        .first()
    )
    
    if variant_specific:
        return variant_specific
    
    return (
        CarDescription.objects
        .filter(
            car_model = variant.car_model,
            variant__isnull=True,
            is_primary=True,
            is_published=True,
        )
        .prefetch_related("sections")
        .first()
    )