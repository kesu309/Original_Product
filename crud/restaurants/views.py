from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Review, Reservation, Favorite, Profile  # 必要なモデルのみインポート
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignUpForm, RestaurantSearchForm, ReviewForm, ProfileForm
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RestaurantSerializer
from datetime import datetime, timedelta

def restaurant_list(request):
    keyword = request.GET.get('keyword', '')
    print(f"検索キーワード: {keyword}")  # デバッグ用

    # 全レストランの取得（評価の高い順）
    restaurants = Restaurant.objects.annotate(
        average_rating_annotated=Avg('reviews__rating')
    ).order_by('-average_rating_annotated')
    print(f"全レストラン数: {restaurants.count()}")  # デバッグ用

    if keyword:
        restaurants = restaurants.filter(
            Q(name__icontains=keyword) |  # 店舗名で検索
            Q(category__name__icontains=keyword) |  # カテゴリ名で検索
            Q(address__icontains=keyword)  # 住所で検索
        ).distinct()
        print(f"検索結果数: {restaurants.count()}")  # デバッグ用

    context = {
        'restaurants': restaurants,
        'keyword': keyword,
    }
    return render(request, 'restaurants/restaurant_list.html', context)

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    reviews = restaurant.reviews.all().order_by('-created_at')
    review_form = ReviewForm()
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
    today = timezone.now().date()
    
    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'reviews': reviews,
        'review_form': review_form,
        'is_favorite': is_favorite,
        'today': today,
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
    restaurant = get_object_or_404(Restaurant, pk=pk)
    # お気に入りの検索
    favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()
    
    if favorite:
        # お気に入りが存在する場合は削除
        favorite.delete()
        messages.success(request, 'お気に入りから削除しました。')
    else:
        # お気に入りが存在しない場合は作成
        Favorite.objects.create(user=request.user, restaurant=restaurant)
        messages.success(request, 'お気に入りに追加しました。')
    
    return redirect('restaurants:restaurant_detail', pk=pk)

@login_required
def add_review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # レビューの作成
            review = Review.objects.create(
                restaurant=restaurant,
                user=request.user,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            messages.success(request, 'レビューを投稿しました。')
    return redirect('restaurants:restaurant_detail', pk=pk)

@login_required
def reservation_list(request):
    today = timezone.now().date()
    reservations = Reservation.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'restaurants/reservation_list.html', {
        'reservations': reservations,
        'today': today
    })

@login_required
def cancel_reservation(request, pk):
    # 予約の取得と削除
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    try:
        reservation.delete()
        messages.success(request, '予約をキャンセルしました。')
    except Exception as e:
        messages.error(request, '予約のキャンセルに失敗しました。')
    
    return redirect('restaurants:reservation_list')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'restaurants/favorite_list.html', {'favorites': favorites})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'restaurants/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # ユーザー情報の更新
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.save()

        # プロフィール情報の更新
        profile = request.user.profile
        profile.username_kana = request.POST.get('username_kana')
        profile.post_code = request.POST.get('post_code')
        profile.address = request.POST.get('address')
        profile.tel = request.POST.get('tel')
        profile.save()

        messages.success(request, '会員情報を更新しました。')
        return redirect('restaurants:profile')

    return render(request, 'restaurants/edit_profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })

# レストランのCRUD操作用のViewSet
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

def restaurant_crud(request):
    """
    レストランのCRUD操作用のビュー
    """
    return render(request, 'restaurants/restaurant_crud.html')

@login_required
def reservation_calendar(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_people = request.POST.get('number_of_people')
        
        try:
            # 予約の作成
            reservation = Reservation.objects.create(
                restaurant=restaurant,
                user=request.user,
                date=date,
                time=time,
                number_of_people=number_of_people
            )
            messages.success(request, '予約が完了しました。')
            return redirect('restaurants:reservation_list')
        except Exception as e:
            messages.error(request, '予約に失敗しました。もう一度お試しください。')
            return redirect('restaurants:reservation_calendar', restaurant_id=restaurant_id)
    
    # 予約可能時間の生成（10:00から21:00まで1時間おき）
    hours = []
    start = datetime.strptime('10:00', '%H:%M').time()
    end = datetime.strptime('21:00', '%H:%M').time()
    current = datetime.combine(datetime.today(), start)
    
    while current.time() <= end:
        hours.append(current.strftime('%H:%M'))
        current += timedelta(hours=1)
    
    # 予約可能人数（1人から10人まで）
    guest_numbers = range(1, 11)
    
    context = {
        'restaurant': restaurant,
        'hours': hours,
        'guest_numbers': guest_numbers,
    }
    
    return render(request, 'restaurants/reservation_calendar.html', context)
