from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from .models import Product


# ========== Задание 1: CBV вместо FBV ==========

class HomeView(ListView):
    """Контроллер для домашней страницы со списком товаров"""
    model = Product  # какую модель берём
    template_name = 'catalog/home.html'  # какой шаблон показываем
    context_object_name = 'products'  # под каким именем передаём в шаблон


class ContactsView(View):
    """Контроллер для страницы контактов с обработкой формы"""

    def get(self, request):
        """GET-запрос — просто показываем страницу"""
        return render(request, 'catalog/contacts.html', {'success': False})

    def post(self, request):
        """POST-запрос — обрабатываем форму"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        success = False
        if name:
            success = True
            print(f"Получено сообщение от {name} ({email}): {message}")

        return render(request, 'catalog/contacts.html', {'success': success})


class ProductDetailView(DetailView):
    """Контроллер для страницы с подробной информацией о товаре"""
    model = Product  # какую модель берём
    template_name = 'catalog/product_detail.html'  # какой шаблон
    context_object_name = 'product'  # под каким именем передаём
    pk_url_kwarg = 'product_id'  # какой параметр из URL использовать как ID