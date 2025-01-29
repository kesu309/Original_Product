from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'restaurants'

# APIルーター
router = DefaultRouter()
router.register(r'api/restaurants', api.RestaurantViewSet, basename='api-restaurant')
router.register(r'api/reviews', api.ReviewViewSet, basename='api-review')
router.register(r'api/reservations', api.ReservationViewSet, basename='api-reservation')
router.register(r'api/favorites', api.FavoriteViewSet, basename='api-favorite')
router.register(r'api/profiles', api.ProfileViewSet, basename='api-profile')

# 既存のURLパターン
urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('premium-plan/', views.premium_plan, name='premium_plan'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # APIルーターのURLを含める
    path('', include(router.urls)),

    # カレンダー予約のURL
    path('restaurant/<int:restaurant_id>/reservation/', views.reservation_calendar, name='reservation_calendar'),
] 