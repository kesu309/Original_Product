from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from restaurants.models import Restaurant

def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            return redirect('restaurant_detail', pk=restaurant_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'restaurant': restaurant})
