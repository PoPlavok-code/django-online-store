from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """Список всех продуктов (ОТКРЫТ ДЛЯ ВСЕХ)"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    # Показываем только опубликованные продукты
    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    """Детальная страница товара (ОТКРЫТ ДЛЯ ВСЕХ)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'

    # Автоматически устанавливаем владельца при создании
    def form_valid(self, form):
        form.instance.owner = self.request.user
        # По умолчанию продукт не опубликован (требует модерации)
        form.instance.is_published = False
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, View):
    """Редактирование продукта (ТОЛЬКО ВЛАДЕЛЕЦ или МОДЕРАТОР)"""

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверяем: владелец ИЛИ модератор с правом can_unpublish_product
        if (product.owner == request.user or
                request.user.has_perm('catalog.can_unpublish_product')):
            form = ProductForm(instance=product)
            return render(request, 'catalog/product_form.html', {'form': form})
        else:
            return redirect('catalog:product_detail', pk=pk)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверяем права
        if (product.owner == request.user or
                request.user.has_perm('catalog.can_unpublish_product')):
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('catalog:product_detail', pk=pk)
        else:
            return redirect('catalog:product_detail', pk=pk)

        return render(request, 'catalog/product_form.html', {'form': form})


class ProductDeleteView(LoginRequiredMixin, View):
    """Удаление продукта (ТОЛЬКО ВЛАДЕЛЕЦ или МОДЕРАТОР)"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверяем: владелец ИЛИ модератор с правом delete_product
        if (product.owner == request.user or
                request.user.has_perm('catalog.delete_product')):
            product.delete()
            return redirect('catalog:product_list')
        else:
            return redirect('catalog:product_detail', pk=pk)