from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time
from multiselectfield import MultiSelectField

class Category(models.Model):
    """
    Stores a shop category, related to :model:`nagoyameshi.Shop`.
    """
    name = models.CharField(max_length=200, verbose_name='名称')
    img = models.ImageField(blank=True, default='noImage.png', verbose_name='画像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')

    def __str__(self):
        return self.name

    def total(self):
        return Shop.objects.filter(category=self.id).count()


class Shop(models.Model):
    """
    Stores a shop, related to :model:`nagoyameshi.Category` and
    :model:`nagoyameshi.Review`.
    """
    TIME_CHOICE = (
        (time(0, 0, 0), '00:00'),
        (time(1, 0, 0), '01:00'),
        (time(2, 0, 0), '02:00'),
        (time(3, 0, 0), '03:00'),
        (time(4, 0, 0), '04:00'),
        (time(5, 0, 0), '05:00'),
        (time(6, 0, 0), '06:00'),
        (time(7, 0, 0), '07:00'),
        (time(8, 0, 0), '08:00'),
        (time(9, 0, 0), '09:00'),
        (time(10, 0, 0), '10:00'),
        (time(11, 0, 0), '11:00'),
        (time(12, 0, 0), '12:00'),
        (time(13, 0, 0), '13:00'),
        (time(14, 0, 0), '14:00'),
        (time(15, 0, 0), '15:00'),
        (time(16, 0, 0), '16:00'),
        (time(17, 0, 0), '17:00'),
        (time(18, 0, 0), '18:00'),
        (time(19, 0, 0), '19:00'),
        (time(20, 0, 0), '20:00'),
        (time(21, 0, 0), '21:00'),
        (time(22, 0, 0), '22:00'),
        (time(23, 0, 0), '23:00'),
    )
    WEEKDAY_CHOICES = (
        ('mon', '月'),
        ('tue', '火'),
        ('wed', '水'),
        ('thu', '木'),
        ('fri', '金'),
        ('sat', '土'),
        ('sun', '日'),
    )
    name = models.CharField(max_length=200, verbose_name='名称')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ')
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ2', related_name='product2')
    category3 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ3', related_name='product3')
    img = models.ImageField(blank=True, default='noImage.png', verbose_name='画像')
    budget_min = models.PositiveIntegerField(verbose_name='最低価格')
    budget_max = models.PositiveIntegerField(verbose_name='最高価格')
    detail = models.TextField(blank=True, null=True, verbose_name='説明')
    address = models.CharField(max_length=200, verbose_name='住所')
    tel = models.CharField(max_length=20, verbose_name='電話番号')
    holiday = MultiSelectField(choices=WEEKDAY_CHOICES, max_length=30, verbose_name='定休日')
    sheet_no = models.PositiveIntegerField(verbose_name='座席数')
    open_from = models.TimeField(choices=TIME_CHOICE, verbose_name='開店時間')
    open_to = models.TimeField(choices=TIME_CHOICE, verbose_name='閉店時間')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')

    def __str__(self):
        return self.name

    def stars_average(self):
        """Average score"""
        average = self.reviews.aggregate(models.Avg('stars'))['stars__avg']
        return round(average, 1) if average is not None else 0

    def data_rate(self):
        """Average score in 0.5 increments"""
        average = self.reviews.aggregate(models.Avg('stars'))['stars__avg']
        average = round(average, 1) if average is not None else 0

        ret = 0
        if average == 5.0:
            ret = 5
        elif average > 4.0:
            ret = 4.5
        elif average == 4.0:
            ret = 4
        elif average > 3.0:
            ret = 3.5
        elif average == 3.0:
            ret = 3
        elif average > 2.0:
            ret = 2.5
        elif average == 2.0:
            ret = 2
        elif average > 1.0:
            ret = 1.5
        elif average == 1.0:
            ret = 1

        return ret

    def review_count(self):
        """Num of reviews"""
        count = self.reviews.aggregate(models.Count('stars'))['stars__count']
        return count

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True, verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}"

class Favorite(models.Model):
    """
    Stores a favorite, related to :model:`nagoyameshi.Shop`.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザ')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='favorites', verbose_name='店舗')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')

class Profile(models.Model):
    """
    Stores a user profile, related to :model:`auth.User`.
    """
    USER_TYPES = (
        ('free', '一般ユーザ'),
        ('payed', '課金ユーザ'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ユーザ')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='free', verbose_name='会員種別')
    username_kana = models.CharField(max_length=20, blank=True, verbose_name='フリガナ')
    post_code = models.CharField(max_length=10, blank=True, verbose_name='郵便番号')
    address = models.CharField(max_length=50, blank=True, verbose_name='住所')
    tel = models.CharField(max_length=20, blank=True, verbose_name='電話番号')
    birth_date = models.DateField(null=True, blank=True, verbose_name='誕生日')
    business = models.CharField(max_length=20, blank=True, verbose_name='職業')
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    stripe_card_name = models.CharField(max_length=255, blank=True)
    stripe_setup_intent = models.CharField(max_length=255, blank=True)
    stripe_card_no = models.CharField(max_length=20, blank=True)
    stripe_card_brand = models.CharField(max_length=20, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update user profile when user is saved"""
    instance.profile.save()

class Reservation(models.Model):
    """
    Stores a shop reservation, related to :model:`nagoyameshi.Shop`.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reservations', verbose_name='店舗')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザ')
    reserv_date = models.DateField(verbose_name='予約日')
    reserv_time = models.TimeField(verbose_name='予約時間')
    num_of_people = models.PositiveIntegerField(verbose_name='予約人数')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "reserv_date", "reserv_time"], name="reservation_unique"),
        ]

class Company(models.Model):
    """
    Stores a company information.
    """
    name = models.CharField(max_length=50, verbose_name='会社名')
    address = models.CharField(max_length=50, verbose_name='所在地')
    president = models.CharField(max_length=20, verbose_name='代表者')
    since = models.CharField(max_length=20, verbose_name='設立')
    budget = models.CharField(max_length=20, verbose_name='資本金')
    business = models.CharField(max_length=50, verbose_name='事業内容')
    people = models.CharField(max_length=20, verbose_name='従業員数')


class Terms(models.Model):
    """
    Stores a terms information.
    """
    contents = models.TextField(verbose_name='利用規約')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')

    def __str__(self):
        return '利用規約'