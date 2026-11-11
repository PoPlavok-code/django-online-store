from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
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
    """Детальная страница товара (ОТКРЫТ ДЛЯ ВСЕХ)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'



# ========== CRUD для продуктов ==========

class ProductListView(ListView):
    """Список всех продуктов (ОТКРЫТ ДЛЯ ВСЕХ)"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'