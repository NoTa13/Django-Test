from django.urls import path
from .views import BlogDetailView

urlpatterns = [
    path('blog/<int:pk>/', BlogDetailView.as_path(), name='blog_detail'),
]