from django.db import models
from django.db.models import Value, BooleanField, Exists, OuterRef

class VariantQuerySet(models.QuerySet):
    def annotate_saved(self, user):
        """
        Annotate adds the 'is_saved' (True/False) field to each vehicle based on the current user.
        """
        if not user or user.is_anonymous:
            return self.annotate(is_saved=Value(False, output_field=BooleanField()))
        
        from users.models import SavedCar
        saved_cars = SavedCar.objects.filter(
            user=user,
            car=OuterRef('pk')
        )
        
        return self.annotate(is_saved=Exists(saved_cars))
    

class VariantManager(models.Manager):
    def get_queryset(self) -> VariantQuerySet:
        return VariantQuerySet(self.model, using=self._db)
    
    def annotate_saved(self, user):
        return self.get_queryset().annotate_saved(user)