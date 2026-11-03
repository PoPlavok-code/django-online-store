from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


# ========== Существующие контроллеры ==========

class HomeView(ListView):
    """Контроллер для домашней страницы со списком товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


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
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


# ========== CRUD для продуктов (новое для домашки 26.1) ==========

class ProductListView(ListView):
    """Список всех продуктов (для CRUD)"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')