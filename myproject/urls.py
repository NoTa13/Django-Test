from django.contrib import admin
from django.urls import path, include
from blog.views import BlogDetailView
from horse_tours.views import TourDetailView, create_booking, add_comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 1. Задание по Блогу (счетчик просмотров)
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    
    # 2. Задание по CRUD
    path('items/', include('crud_app.urls')),
    
    # 3. Задание по Конным турам
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('tours/<int:tour_id>/book/', create_booking, name='create_booking'),
    path('tours/<int:tour_id>/comment/', add_comment, name='add_comment'),
]