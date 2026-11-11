from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.action(description='Опубликовать выбранные продукты')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Снять с публикации выбранные продукты')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Product)  # ← ТОЛЬКО ОДНА ТАКАЯ СТРОКА!
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_published', 'owner')
    list_filter = ('is_published', 'category')
    search_fields = ('name',)
    actions = [make_published, make_unpublished]