
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


class RegisterView(View):
    """Регистрация пользователя"""

    def get(self, request):
        """Показываем форму регистрации"""
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        """Обрабатываем регистрацию"""
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Отправляем приветственное письмо
            send_mail(
                subject='Добро пожаловать в наш магазин!',
                message=f'Здравствуйте, {user.email}!\n\nСпасибо за регистрацию в нашем интернет-магазине.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Автоматически входим пользователя
            login(request, user)
            return redirect('catalog:product_list')

        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    """Авторизация пользователя"""

    def get(self, request):
        """Показываем форму входа"""
        form = CustomAuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        """Обрабатываем вход"""
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog:product_list')

        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    """Выход пользователя"""

    def post(self, request):
        logout(request)
        return redirect('catalog:product_list')


class ProfileUpdateView(LoginRequiredMixin, View):
    """Редактирование профиля пользователя"""

    def get(self, request):
        """Показываем форму редактирования"""
        form = UserProfileForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        """Сохраняем изменения"""
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'users/profile.html', {'form': form})
