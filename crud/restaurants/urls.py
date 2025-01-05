from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:pk>/reserve/', views.make_reservation, name='make_reservation'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
] 