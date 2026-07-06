from django.db.models import QuerySet, Value, BooleanField, Exists, OuterRef
from users.models import SavedCar

def annotate_saved(qs: QuerySet, user):
    if not user.is_authenticated:
        return qs.annotate(
            is_saved=Value(False, output_field=BooleanField())
        )
        
    return qs.annotate(
        is_saved=Exists(
            SavedCar.objects.filter(
                user=user,
                car=OuterRef("pk")
            )
        )
    )