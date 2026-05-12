from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'city', 'book_count', 'rating_average')
    list_filter = ('gender', 'city', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {'fields': ('phone', 'gender', 'city', 'profile_photo')}),
        ('İstatistikler', {'fields': ('book_count', 'rating_average', 'rating_count')}),
    )
