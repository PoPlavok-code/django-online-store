from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Очищает БД и загружает тестовые данные из фикстуры'

    def handle(self, *args, **options):
        # Предварительное удаление данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('Старые данные успешно удалены.'))

        # Загрузка данных из фикстуры
        call_command('loaddata', 'products.json')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены из фикстуры!'))