from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, SavedCar

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Hồ Sơ"
    

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(SavedCar)
class SavedCarAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'car__name']

