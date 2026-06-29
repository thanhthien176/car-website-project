from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import User, SavedCar, SalerProfile, Showroom, Province


# Register your models here.

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "slug"]
    search_fields = ["name", "code"]
    
    
@admin.register(Showroom)
class ShowroomAdmin(admin.ModelAdmin):
    list_display = [
        "brand", "name", "province", "address"
    ]
    list_filter = ["brand", "province"]
    search_fields = ["brand", "province", "name"]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Extends Django's built-in UserAdmin to display custom fields.
    BaseUserAdmin already handles password hashing, permission, groups, 
    We only add our extra field on top.
    """
    # Add custom fields to the detail view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Thông tin cá nhân", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Phân quyền", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
            ),
            "classes": ("collapse",),
        }),
        ("Thời gian", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
        ("Thông tin bổ sung", {
            "fields": ("bio", "avatar", "province", "birth_year", "user_type",),
            "classes": ("collapse", ),
        }),
        ("Thông tin nhạy cảm", {
            "fields":("phone_encrypted", "phone_hash", "address_encrypted"),
            "classes": ("collapse",),
        })
    )
    
    list_display =[
        "username", "email", "display_name", "user_type",
        "province", "is_active", "date_joined",
    ]
    list_filter = ["user_type", "is_active", "province"]
    search_fields = ["username", "email", "first_name", "last_name"]
    
    def has_delete_permission(self, request: HttpRequest, obj= None) -> bool:
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        """Prevent bulk deletion of superuser accounts."""
        protected = queryset.filter(is_superuser=True)
        if protected.exists():
            names = ", ".join(protected.values_list("username", flat=True))
            self.message_user(
                request,
                f"Không thể xóa superuser: {names}",
                level = messages.ERROR
            )
            queryset = queryset.filter(is_superuser=False)
            
        super().delete_queryset(request, queryset)
    
    def get_readonly_fields(self, request: HttpRequest, obj= None):
        """
        Prevent non-superusers from editing superuser flag.
        Only a superuser can grant/revoke superuser status.
        """
        
        readonly = list(super().get_readonly_fields(request, obj))
        
        User = get_user_model()
        user = request.user
        if isinstance(user, User) and not user.is_superuser:
            readonly.append('is_superuser')
        return readonly

@admin.register(SalerProfile)
class SalerProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user", "showroom", "is_verified", "verified_at"        
    ]
    list_filter = ["is_verified", "showroom"]
    search_fields = [
        "user__username", "user__email",
        "showroom__name", "employee_id",
    ]
    readonly_fields = ["cccd_encrypted", "cccd_hash", "verified_at"]
    
    fieldsets = (
        ("Thông tin cơ bản",{
            "fields":("user", "showroom", "employee_id"),
        }),
        ("CCCD encrypted", {
          "fields": ("cccd_encrypted", "cccd_hash"), 
        }),
        ("Xác minh", {
            "fields": ("is_verified", "verified_at"),
        }),
    )
    
@admin.register(SavedCar)
class SavedCarAdmin(admin.ModelAdmin):
    list_display = ["user", "car", "saved_at"]
    list_filter = ["saved_at"]
    search_fields = ["user__username", "car_name"]