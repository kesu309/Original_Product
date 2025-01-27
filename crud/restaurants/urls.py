from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('<int:pk>/reservation/', views.make_reservation, name='make_reservation'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('premium-plan/', views.premium_plan, name='premium_plan'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
] 