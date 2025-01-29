from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='カテゴリー名')
    slug = models.SlugField(unique=True, verbose_name='スラッグ')
    description = models.TextField(blank=True, verbose_name='説明')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー一覧'
        ordering = ['name']

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    AREA_CHOICES = [
        ('higashi', '福岡市東区'),
        ('chuo', '福岡市中央区'),
        ('hakata', '福岡市博多区'),
        ('minami', '福岡市南区'),
        ('nishi', '福岡市西区'),
        ('jonan', '福岡市城南区'),
        ('sawara', '福岡市早良区'),
    ]
    
    PRICE_RANGE_CHOICES = [
        ('budget', '~¥1,000'),
        ('low', '¥1,000~¥2,000'),
        ('middle', '¥2,000~¥4,000'),
        ('high', '¥4,000~¥8,000'),
        ('expensive', '¥8,000~'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='店舗名')
    description = models.TextField(verbose_name='店舗説明', blank=True)
    price_range = models.CharField(
        max_length=20,
        choices=PRICE_RANGE_CHOICES,
        default='middle',
        verbose_name='価格帯'
    )
    post_code = models.CharField(max_length=7, verbose_name='郵便番号')
    address = models.CharField(max_length=200, verbose_name='住所', blank=True, default='')
    category = models.CharField(
        max_length=50,
        verbose_name='カテゴリー'
    )
    area = models.CharField(
        max_length=20, 
        choices=AREA_CHOICES, 
        default='other',
        verbose_name='エリア'
    )
    opening_time = models.TimeField(default='11:00', verbose_name='開店時間')
    closing_time = models.TimeField(default='22:00', verbose_name='閉店時間')
    closed_days = models.CharField(max_length=100, verbose_name='定休日', blank=True)

    class Meta:
        verbose_name = 'レストラン'
        verbose_name_plural = 'レストラン一覧'
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_open_at(self, time):
        return self.opening_time <= time <= self.closing_time

    @property
    def average_rating(self):
        """レストランの平均評価を計算する"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

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
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='reservations',
        verbose_name='店舗'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='ユーザー'
    )
    date = models.DateField(
        verbose_name='予約日',
        error_messages={
            'invalid': '正しい日付の形式で入力してください。',
            'required': '予約日を入力してください。'
        }
    )
    time = models.TimeField(
        verbose_name='予約時間',
        error_messages={
            'invalid': '正しい時間の形式で入力してください。',
            'required': '予約時間を入力してください。'
        }
    )
    number_of_people = models.IntegerField(
        validators=[MinValueValidator(1, message='1名以上を入力してください。')],
        verbose_name='人数',
        error_messages={
            'invalid': '正しい人数を入力してください。',
            'required': '人数を入力してください。'
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約一覧'
        ordering = ['date', 'time']
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "time"],
                name="reservation_unique"
            ),
        ]

    def get_japanese_weekday(self):
        weekday_dict = {
            0: '月',
            1: '火',
            2: '水',
            3: '木',
            4: '金',
            5: '土',
            6: '日'
        }
        return weekday_dict[self.date.weekday()]

    def __str__(self):
        formatted_date = self.date.strftime('%Y/%m/%-d')
        formatted_time = self.time.strftime('%H:%M')
        weekday = self.get_japanese_weekday()
        return f"{self.restaurant.name} - {formatted_date}（{weekday}） {formatted_time}"

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
    username_kana = models.CharField(max_length=100, default='', verbose_name='フリガナ')
    post_code = models.CharField(max_length=7, default='', verbose_name='郵便番号')
    address = models.CharField(max_length=200, default='', verbose_name='住所')
    tel = models.CharField(max_length=11, default='', verbose_name='電話番号')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='ニックネーム')
    bio = models.TextField(blank=True, verbose_name='自己紹介')
    favorite_cuisine = models.CharField(max_length=100, blank=True, verbose_name='好きな料理')

    def __str__(self):
        return self.user.username
