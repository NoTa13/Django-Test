# horse_tours/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Tour, Category, Booking, Comment

class HorseTourStartupTests(TestCase):

    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(username='rider1', password='password123')
        self.user2 = User.objects.create_user(username='rider2', password='password123')

        # 1. Тестируем связи Многие-ко-многим (Categories <-> Tour)
        self.cat_horse = Category.objects.create(name="Конный")
        self.cat_hike = Category.objects.create(name="Пеший")
        self.cat_moto = Category.objects.create(name="На мото")

        self.tour = Tour.objects.create(
            title="Конный тур по Тянь-Шаню",
            description="Увлекательное путешествие верхом на лошадях"
        )
        self.tour.categories.add(self.cat_horse, self.cat_hike)

        self.now = timezone.now()

    # --- ТЕСТ 1: Проверка связи Многие-ко-Многим ---
    def test_many_to_many_tour_categories(self):
        self.assertEqual(self.tour.categories.count(), 2)
        self.assertIn(self.cat_horse, self.tour.categories.all())
        self.assertIn(self.cat_hike, self.tour.categories.all())

    # --- ТЕСТ 2: Проверка ограничения (1 человек = 1 тур на конкретное время) ---
    def test_one_booking_per_user_per_timeslot(self):
        self.client.login(username='rider1', password='password123')
        url = reverse('create_booking', kwargs={'tour_id': self.tour.id})
        
        # Первое бронирование — успешно
        response1 = self.client.post(url, {'date_time': self.now})
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

        # Повторное бронирование на ту же дату и время этим же пользователем — ошибка 400
        response2 = self.client.post(url, {'date_time': self.now})
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(Booking.objects.count(), 1)

    # --- ТЕСТ 3: Проверка связи 1-ко-многим (1 человек = несколько комментариев) ---
    def test_user_can_leave_multiple_comments(self):
        # Создаем бронирование для доступа к комментариям
        Booking.objects.create(user=self.user1, tour=self.tour, date_time=self.now)
        
        self.client.login(username='rider1', password='password123')
        url = reverse('add_comment', kwargs={'tour_id': self.tour.id})

        # Отправка 1-го комментария
        self.client.post(url, {'text': 'Отличный лошадиный маршрут!'})
        # Отправка 2-го комментария от того же пользователя
        self.client.post(url, {'text': 'Инструктор супер!'})

        self.assertEqual(Comment.objects.filter(user=self.user1).count(), 2)

    # --- ТЕСТ 4: Отказ в отправке комментария, если пользователь не посещал тур ---
    def test_comment_forbidden_without_booking(self):
        self.client.login(username='rider2', password='password123')
        url = reverse('add_comment', kwargs={'tour_id': self.tour.id})

        response = self.client.post(url, {'text': 'Я тут не был, но пишу'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), 0)