from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Review, Reservation, Favorite, Profile  # 必要なモデルのみインポート
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignUpForm, RestaurantSearchForm, ReviewForm, ReservationForm, ProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

def restaurant_list(request):
    keyword = request.GET.get('keyword', '')
    restaurants = Restaurant.objects.all()

    if keyword:
        restaurants = restaurants.filter(
            Q(name__icontains=keyword) |  # 店舗名で検索
            Q(category__in=[choice[0] for choice in Restaurant.CATEGORY_CHOICES if keyword.lower() in choice[1].lower()]) |  # カテゴリで検索
            Q(area__in=[choice[0] for choice in Restaurant.AREA_CHOICES if keyword.lower() in choice[1].lower()])  # エリアで検索
        ).distinct()

    context = {
        'restaurants': restaurants,
        'keyword': keyword,
    }
    return render(request, 'restaurants/restaurant_list.html', context)

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '新規登録が完了しました。')
            return redirect('restaurants:restaurant_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def toggle_favorite(request, pk):
    """お気に入りの切り替えを処理する"""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()
    
    if favorite:
        # お気に入りが存在する場合は削除
        favorite.delete()
        is_favorite = False
    else:
        # お気に入りが存在しない場合は作成
        Favorite.objects.create(user=request.user, restaurant=restaurant)
        is_favorite = True
    
    # ユーザーのお気に入りリストを更新
    request.user.favorite_set.clear()
    request.user.favorite_set.add(*Favorite.objects.filter(user=request.user).values_list('restaurant', flat=True))
    
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def add_review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            messages.success(request, 'レビューを投稿しました。')
            return redirect('restaurants:restaurant_detail', pk=pk)
    return redirect('restaurants:restaurant_detail', pk=pk)

@login_required
def make_reservation(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.user = request.user
            reservation.save()
            messages.success(request, '予約が完了しました。')
            return redirect('restaurants:restaurant_detail', pk=pk)
    else:
        form = ReservationForm()
    return render(request, 'restaurants/reservation_form.html', {
        'form': form,
        'restaurant': restaurant
    })

@login_required
def profile_view(request):
    # プロフィールが存在しない場合は作成
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'restaurants/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('restaurants:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'restaurants/edit_profile.html', {'form': form})

@login_required
def reservation_list(request):
    today = timezone.now().date()
    reservations = Reservation.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'restaurants/reservations.html', {
        'reservations': reservations,
        'today': today
    })

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, '予約をキャンセルしました。')
    return redirect('restaurants:reservation_list')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'restaurants/favorites.html', {
        'favorites': favorites
    })
