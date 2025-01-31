# Generated by Django 5.1.4 on 2025-01-29 16:23

import django.core.validators
import django.db.models.deletion
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="カテゴリー名")),
                (
                    "img",
                    models.ImageField(
                        blank=True,
                        default="noImage.png",
                        upload_to="",
                        verbose_name="画像",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="説明")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "カテゴリー",
                "verbose_name_plural": "カテゴリー一覧",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="会社名")),
                ("address", models.CharField(max_length=50, verbose_name="所在地")),
                ("president", models.CharField(max_length=20, verbose_name="代表者")),
                ("since", models.CharField(max_length=20, verbose_name="設立")),
                ("budget", models.CharField(max_length=20, verbose_name="資本金")),
                ("business", models.CharField(max_length=50, verbose_name="事業内容")),
                ("people", models.CharField(max_length=20, verbose_name="従業員数")),
            ],
            options={
                "verbose_name": "会社情報",
                "verbose_name_plural": "会社情報",
            },
        ),
        migrations.CreateModel(
            name="Terms",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contents", models.TextField(verbose_name="利用規約")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "利用規約",
                "verbose_name_plural": "利用規約",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username_kana",
                    models.CharField(
                        default="", max_length=100, verbose_name="フリガナ"
                    ),
                ),
                (
                    "post_code",
                    models.CharField(default="", max_length=7, verbose_name="郵便番号"),
                ),
                (
                    "address",
                    models.CharField(default="", max_length=200, verbose_name="住所"),
                ),
                (
                    "tel",
                    models.CharField(
                        default="", max_length=11, verbose_name="電話番号"
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="誕生日"),
                ),
                (
                    "business",
                    models.CharField(blank=True, max_length=20, verbose_name="職業"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="店舗名")),
                ("description", models.TextField(blank=True, verbose_name="店舗説明")),
                (
                    "price_range",
                    models.CharField(
                        choices=[
                            ("budget", "~¥1,000"),
                            ("low", "¥1,000~¥2,000"),
                            ("middle", "¥2,000~¥4,000"),
                            ("high", "¥4,000~¥8,000"),
                            ("expensive", "¥8,000~"),
                        ],
                        default="middle",
                        max_length=20,
                        verbose_name="価格帯",
                    ),
                ),
                ("post_code", models.CharField(max_length=7, verbose_name="郵便番号")),
                ("address", models.CharField(max_length=200, verbose_name="住所")),
                ("tel", models.CharField(max_length=20, verbose_name="電話番号")),
                (
                    "area",
                    models.CharField(
                        choices=[
                            ("higashi", "福岡市東区"),
                            ("chuo", "福岡市中央区"),
                            ("hakata", "福岡市博多区"),
                            ("minami", "福岡市南区"),
                            ("nishi", "福岡市西区"),
                            ("jonan", "福岡市城南区"),
                            ("sawara", "福岡市早良区"),
                        ],
                        default="other",
                        max_length=20,
                        verbose_name="エリア",
                    ),
                ),
                (
                    "opening_time",
                    models.TimeField(default="11:00", verbose_name="開店時間"),
                ),
                (
                    "closing_time",
                    models.TimeField(default="22:00", verbose_name="閉店時間"),
                ),
                (
                    "closed_days",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("mon", "月"),
                            ("tue", "火"),
                            ("wed", "水"),
                            ("thu", "木"),
                            ("fri", "金"),
                            ("sat", "土"),
                            ("sun", "日"),
                        ],
                        max_length=30,
                        verbose_name="定休日",
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        blank=True,
                        default="noImage.png",
                        upload_to="",
                        verbose_name="画像",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurants.category",
                        verbose_name="カテゴリー",
                    ),
                ),
            ],
            options={
                "verbose_name": "レストラン",
                "verbose_name_plural": "レストラン一覧",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="評価",
                    ),
                ),
                ("comment", models.TextField(verbose_name="コメント")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="restaurants.restaurant",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "レビュー",
                "verbose_name_plural": "レビュー一覧",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(verbose_name="予約日")),
                ("time", models.TimeField(verbose_name="予約時間")),
                (
                    "number_of_people",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="人数",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="restaurants.restaurant",
                        verbose_name="店舗",
                    ),
                ),
            ],
            options={
                "verbose_name": "予約",
                "verbose_name_plural": "予約一覧",
                "ordering": ["date", "time"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user", "date", "time"), name="reservation_unique"
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorites",
                        to="restaurants.restaurant",
                    ),
                ),
            ],
            options={
                "verbose_name": "お気に入り",
                "verbose_name_plural": "お気に入り一覧",
                "unique_together": {("restaurant", "user")},
            },
        ),
    ]
