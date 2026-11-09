# horse_tours/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")

    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    # Связь Многие-ко-многим (ManyToManyField)
    categories = models.ManyToManyField(Category, related_name="tours", verbose_name="Категории")

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    date_time = models.DateTimeField(verbose_name="Дата и время")

    class Meta:
        # Связь 1-к-1 для ограничения: 1 человек на 1 конкретное время (слот)
        unique_together = ('user', 'date_time')

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.date_time})"

class Comment(models.Model):
    # Связь 1-ко-многим (ForeignKey): 1 человек может оставлять много комментариев
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.tour.title}"