from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Restaurant(models.Model):
    CATEGORY_CHOICES = [
        ('japanese', '和食'),
        ('chinese', '中華'),
        ('italian', 'イタリアン'),
        ('french', 'フレンチ'),
        ('asian', 'アジアン'),
        ('other', 'その他'),
    ]
    
    AREA_CHOICES = [
        ('shibuya', '渋谷'),
        ('shinjuku', '新宿'),
        ('ikebukuro', '池袋'),
        ('ginza', '銀座'),
        ('roppongi', '六本木'),
        ('other', 'その他'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='店舗名')
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other',
        verbose_name='カテゴリ'
    )
    area = models.CharField(
        max_length=20, 
        choices=AREA_CHOICES, 
        default='other',
        verbose_name='エリア'
    )
    opening_time = models.TimeField(default='11:00', verbose_name='開店時間')
    closing_time = models.TimeField(default='23:00', verbose_name='閉店時間')

    def __str__(self):
        return self.name

    def is_open_at(self, time):
        return self.opening_time <= time <= self.closing_time

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='評価'
    )
    comment = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー一覧'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}のレビュー"

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='予約日')
    time = models.TimeField(verbose_name='予約時間')
    number_of_people = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='人数'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約一覧'
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.restaurant.name} - {self.date} {self.time}"

class Favorite(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り一覧'
        unique_together = ['restaurant', 'user']  # 重複を防ぐ

    def __str__(self):
        return f"{self.user.username}が{self.restaurant.name}をお気に入り登録"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username_kana = models.CharField(max_length=100, default='')
    post_code = models.CharField(max_length=7, default='')
    address = models.CharField(max_length=200, default='')
    tel = models.CharField(max_length=11, default='')

    def __str__(self):
        return self.user.username
