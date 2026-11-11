from django.db import models
from users.models import CustomUser  # импорт твоей кастомной модели


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='catalog/products/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    # ===== НОВОЕ: статус публикации =====
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )

    # ===== НОВОЕ: владелец продукта =====
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True,  # временно, пока не заполним старые продукты
        blank=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at', 'name']
        # ===== НОВОЕ: кастомное право =====
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return f'{self.name} ({self.category.name})'