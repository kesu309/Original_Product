from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Review

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})
