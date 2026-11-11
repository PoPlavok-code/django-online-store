from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группы с правами доступа'

    def handle(self, *args, **options):
        # Получаем тип контента для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # 1. Получаем или создаем НАШЕ кастомное право
        permission_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            defaults={
                'name': 'Может отменять публикацию продукта',
                'content_type': content_type,
            }
        )

        # 2. ПОЛУЧАЕМ стандартное право на удаление (оно уже создано Django!)
        try:
            permission_delete = Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не найдено стандартное право delete_product'))
            return

        # 3. Создаем или получаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Создана группа "Модератор продуктов"'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" уже существует'))

        # 4. Добавляем права в группу
        moderator_group.permissions.add(permission_unpublish, permission_delete)
        self.stdout.write(self.style.SUCCESS('Права успешно добавлены группе "Модератор продуктов"'))

        # 5. Доп. задание: Группа "Контент-менеджер"
        try:
            from blog.models import Post
            blog_content_type = ContentType.objects.get_for_model(Post)

            content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
            if created:
                self.stdout.write(self.style.SUCCESS('Создана группа "Контент-менеджер"'))

            # Получаем все права на модель Post и добавляем их в группу
            blog_permissions = Permission.objects.filter(content_type=blog_content_type)
            content_manager_group.permissions.set(blog_permissions)
            self.stdout.write(self.style.SUCCESS('Права успешно добавлены группе "Контент-менеджер"'))

        except ImportError:
            self.stdout.write(self.style.WARNING('Приложение blog не найдено, пропускаем настройку контент-менеджера'))

        self.stdout.write(self.style.SUCCESS('\nВсе группы созданы и настроены успешно!'))