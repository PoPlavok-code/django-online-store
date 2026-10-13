from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    """Контроллер для домашней страницы со списком товаров"""
    # Получаем все товары из базы данных
    products = Product.objects.all()

    # Передаём их в шаблон под именем 'products'
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    """Контроллер для страницы контактов с обработкой формы"""
    success = False

    # Если форма отправлена методом POST
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Простая проверка, что имя введено
        if name:
            success = True
            # Здесь в будущем будет код отправки на почту или сохранения в БД
            print(f"Получено сообщение от {name} ({email}): {message}")

    context = {
        'success': success
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, product_id):
    """Контроллер для страницы с подробной информацией о товаре (Задание 1)"""
    # get_object_or_404 ищет товар по id. Если не находит, автоматически показывает ошибку 404
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'catalog/product_detail.html', {'product': product})