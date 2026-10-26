from django.contrib import admin
from django.urls import path, include
from blog.views import BlogDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('items/', include('crud_app.urls')),  # <--- Подключили CRUD
]