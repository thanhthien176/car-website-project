from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null= True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Hồ Sơ Người Dùng'
        verbose_name_plural = 'Hồ Sơ Người Dùng'
        
    def __str__(self):
        return f"Profile: {self.user.username}"    

class SavedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_cars')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'car']
        ordering = ['saved_at']
        verbose_name = "Xe đã lưu"
        
    def __str__(self):
        return f"{self.user.username} -> {self.car.name}"
    
    
    