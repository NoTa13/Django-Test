from django.test import TestCase
from django.urls import reverse
from .models import Blog

class BlogDetailViewTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(
            title="Тестовая статья",
            content="Содержимое тестовой статьи"
        )

    # 1. Проверка получения контента
    def test_detail_view_returns_content(self):
        url = reverse('blog_detail', kwargs={'pk': self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Содержимое тестовой статьи")

    # 2. Проверка соответствия ID и объекта в контексте
    def test_detail_view_correct_id_in_context(self):
        url = reverse('blog_detail', kwargs={'pk': self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.context['object'].id, self.blog.id)
        self.assertEqual(response.context['object'].title, "Тестовая статья")

    # 3. Проверка обработки несуществующего ID (404)
    def test_detail_view_nonexistent_id_returns_404(self):
        url = reverse('blog_detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 4. Проверка перехода по URL (корректность разрешения маршрута)
    def test_detail_view_url_resolves_correctly(self):
        url = reverse('blog_detail', kwargs={'pk': self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.view_name, 'blog_detail')

    # 5. Проверка генерации контента при отсутствии текста
    def test_detail_view_empty_content_handling(self):
        empty_blog = Blog.objects.create(title="Пустой блог", content="")
        url = reverse('blog_detail', kwargs={'pk': empty_blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пустой блог")


class BlogViewsCounterTests(TestCase):
    # Тест 1: Проверка, что у нового блога счетчик изначально равен 0
    def test_new_blog_initial_views_is_zero(self):
        blog = Blog.objects.create(title="Новый блог", content="Текст")
        self.assertEqual(blog.views_count, 0)

    # Тест 2: Имитация GET-запроса и проверка увеличения счетчика до 1
    def test_blog_detail_view_increments_views_count(self):
        blog = Blog.objects.create(title="Популярная статья", content="Текст")
        url = reverse('blog_detail', kwargs={'pk': blog.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        blog.refresh_from_db()
        self.assertEqual(blog.views_count, 1)