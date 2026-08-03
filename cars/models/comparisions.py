from django.db import models

from .car_models import CarVariant

class Comparison(models.Model):
    session_key = models.CharField(max_length=40, blank=True)
    cars = models.ManyToManyField(CarVariant, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Car Comparison"
    
    def __str__(self):
        car_names = ", ".join(car.variant_name for car in self.cars.all()) 
        return f"So sánh: {car_names or "Chưa có xe"}"
    
    def can_add_car(self):
        # Maximum of 3 vehicles per comparison.
        return self.cars.count() < 3
    