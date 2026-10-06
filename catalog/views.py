from django.shortcuts import render


def home_view(request):
    """Контроллер для домашней страницы"""
    return render(request, 'catalog/home.html')


def contacts_view(request):
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