from django.contrib import admin
from .models import Restaurant, Review, Reservation, Favorite, Profile

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'area', 'opening_time', 'closing_time')
    list_filter = ('category', 'area')
    search_fields = ('name',)
    ordering = ('name',)
    
    # フィールドの日本語表示
    def get_list_display(self, request):
        return ('name', 'category', 'area', 'opening_time', 'closing_time')
    
    # モデル名の日本語表示
    class Meta:
        verbose_name = '店舗'
        verbose_name_plural = '店舗一覧'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'user__username')
    ordering = ('-created_at',)
    
    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー一覧'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'date', 'time', 'number_of_people')
    list_filter = ('date', 'time')
    search_fields = ('restaurant__name', 'user__username')
    ordering = ('-date', '-time')
    
    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約一覧'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('restaurant__name', 'user__username')
    ordering = ('-created_at',)
    
    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り一覧'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username_kana', 'tel')
    search_fields = ('user__username', 'username_kana', 'tel')
    ordering = ('user__username',)
    
    class Meta:
        verbose_name = '会員情報'
        verbose_name_plural = '会員情報一覧'
