from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import Tour, Booking, Comment

class TourDetailView(DetailView):
    model = Tour
    template_name = 'horse_tours/tour_detail.html'

def create_booking(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=tour_id)
        date_time = request.POST.get('date_time')
        
        # Получаем текущего пользователя или гарантированно берем/создаем существующего
        if request.user.is_authenticated:
            user = request.user
        else:
            user, _ = User.objects.get_or_create(username='guest_rider')
        
        # Проверка ограничения: 1 человек = 1 слот на конкретное время
        if Booking.objects.filter(user=user, date_time=date_time).exists():
            return render(request, 'horse_tours/tour_detail.html', {
                'object': tour,
                'error': 'Вы уже забронировали тур на эту дату и время!'
            }, status=400)
            
        Booking.objects.create(user=user, tour=tour, date_time=date_time)
        return redirect('tour_detail', pk=tour.pk)

def add_comment(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=tour_id)
        text = request.POST.get('text')
        
        if request.user.is_authenticated:
            user = request.user
        else:
            user, _ = User.objects.get_or_create(username='guest_rider')

        Comment.objects.create(user=user, tour=tour, text=text)
        return redirect('tour_detail', pk=tour.pk)