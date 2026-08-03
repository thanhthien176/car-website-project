from django.db import models

from .car_models import CarModel

class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} star") for i in range(1,6)]
    
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pros = models.TextField(blank=True, help_text="Ưu điểm")
    cons = models.TextField(blank=True, help_text="Nhược điểm")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rating', 'is_approved'])
        ]
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        
    def __str__(self):
        return f"{self.author_name} - {self.car} ({self.rating}*)"