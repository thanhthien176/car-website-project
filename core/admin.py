from atexit import register
from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from django.http.response import HttpResponse

from core.models import ContactMe, SiteIdentify


@admin.register(SiteIdentify)
class SiteIdentifyAdmin(admin.ModelAdmin):
    list_display = ['slogan', 'og_title', 'og_description', 'og_image', 'is_active', 'updated_at']
    list_filter = ['slogan', 'og_title', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    
    
@admin.register(ContactMe)
class ContactMeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'status', 'created_at', 'resolution_note', 'done_at')
    list_filter = ('status', 'created_at', 'done_at')
    ordering = ('created_at', 'done_at')
    
    
    readonly_fields = ('created_at', 'done_at')
    
    fieldsets = (
        ('Thông tin khách hàng', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Trạng thái xử lý', {
            'fields': ('status', 'resolution_note', 'done_at')
        }),
    )
    
    def change_view(self, request: HttpRequest, object_id: str, form_url: str = '', extra_context: dict[str, Any] | None = None) -> HttpResponse:
        obj = self.get_object(request, object_id)
        if obj and obj.status == ContactMe.Status.UNREAD:
            obj.status = ContactMe.Status.PROCESSING
            obj.save(update_fields=['status'])
            
            return super().change_view(request, object_id, form_url, extra_context) 
        
        return super().change_view(request, object_id, form_url, extra_context)