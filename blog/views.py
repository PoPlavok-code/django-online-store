from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post


class PostListView(ListView):
    """Список всех опубликованных статей"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Показываем только опубликованные статьи
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    """Детальная страница одной статьи"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        # Показываем только опубликованные статьи
        return Post.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        # Увеличиваем счётчик просмотров
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class PostCreateView(CreateView):
    """Создание новой статьи"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    """Редактирование статьи"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        # После редактирования перенаправляем на страницу статьи
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    """Удаление статьи"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')