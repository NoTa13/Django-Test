# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    views_count = models.PositiveIntegerField(default=0)  # Счетчик просмотров/лайков

    def __str__(self):
        return self.title