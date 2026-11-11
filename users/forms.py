
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле username из формы
        if 'username' in self.fields:
            del self.fields['username']


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа пользователя"""

    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class UserProfileForm(forms.ModelForm):
        """Форма редактирования профиля пользователя"""

        class Meta:
            model = CustomUser
            fields = ['avatar', 'phone', 'country']
            widgets = {
                'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
                'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите страну'}),
            }


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ['avatar', 'phone', 'country']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите страну'}),
        }