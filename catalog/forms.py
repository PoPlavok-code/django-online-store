from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import os

# Список запрещённых слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


def validate_forbidden_words(value):
    """Проверяет, что в тексте нет запрещённых слов"""
    value_lower = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in value_lower:
            raise ValidationError(
                f'Текст содержит запрещённое слово: "{word}"'
            )
    return value


def validate_image(image):
    """Проверяет формат и размер изображения (доп. задание)"""
    if image:
        # Проверка размера (5 МБ)
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError(
                f'Размер файла не должен превышать 5 МБ. '
                f'Текущий размер: {image.size / 1024 / 1024:.2f} МБ'
            )

        # Проверка формата
        ext = os.path.splitext(image.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in valid_extensions:
            raise ValidationError(
                f'Недопустимый формат файла. Разрешены: {", ".join(valid_extensions)}'
            )

    return image


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product

        fields = ['name', 'description', 'price', 'category', 'image']  # ← добавь 'image'

    # Задание 1: валидация запрещённых слов
    name = forms.CharField(
        max_length=200,
        validators=[validate_forbidden_words],
        label='Название продукта'
    )
    description = forms.CharField(
        widget=forms.Textarea(),
        validators=[validate_forbidden_words],
        label='Описание'
    )

    # Доп. задание: валидация изображения (если есть поле image)
    # image = forms.ImageField(
    #     required=False,
    #     validators=[validate_image],
    #     help_text='Формат: JPEG или PNG. Максимум 5 МБ.'
    # )

    # Задание 2: валидация цены
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной!')
        return price

    # Задание 3: стилизация форм через __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-класс ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if hasattr(field, 'label') and field.label:
                field.widget.attrs['placeholder'] = f'Введите {field.label.lower()}'
