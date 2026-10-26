# views.py
from django.views.generic import DetailView
from django.db.models import F
from .models import Blog

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Атомарно увеличиваем счетчик на 1 при каждом посещении
        Blog.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj