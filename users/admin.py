from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомного пользователя"""

    # Поля, которые отображаются в списке пользователей
    list_display = ('email', 'username', 'phone', 'country', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'country')
    search_fields = ('email', 'username', 'phone')

    # Поля для редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('username', 'phone', 'country', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'phone', 'country'),
        }),
    )