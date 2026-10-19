from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое", blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры/Лайки")

    def __str__(self):
        return self.title