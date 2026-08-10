from django.utils import timezone
from django.db import models


class ContactMe(models.Model):
    
    class Status(models.TextChoices):
        UNREAD = 'UNREAD', 'Chưa đọc'
        PROCESSING = 'PROCESSING', 'Đang xử lý'
        DONE = 'DONE', 'Đã xử lý xong'
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNREAD,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    done_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời điểm xử lý xong")
    
    resolution_note =models.TextField(blank=True, verbose_name="Ghi chú phản hồi")
    
    class Meta:
        verbose_name_plural = 'Contacts'
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.DONE and not self.done_at:
            self.done_at = timezone.now()
            
        elif self.status != self.Status.DONE:
            self.done_at = None

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} - {self.subject}'
    

class SiteIdentify(models.Model):
    slogan = models.CharField(max_length=400, blank=True, help_text="Slogan of website")
    
    og_title = models.CharField(max_length=150, blank=True, help_text="Tiêu đề hiển thị khi chia sẻ link")
    og_description = models.CharField(max_length=300, blank=True, help_text="Mô tả ngắn khi chia sẻ link")
    og_image = models.ImageField(upload_to="identify/og/", help_text="Ảnh preview khi chia sẻ Social Media (Tỉ lệ chuẩn 1200x630)")
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)