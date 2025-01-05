# Generated by Django 5.1.4 on 2025-01-03 11:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0002_reservation_review_favorite"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                        blank=True, max_length=100, null=True, verbose_name="フリガナ"
                    ),
                ),
                (
                    "post_code",
                    models.CharField(
                        blank=True, max_length=7, null=True, verbose_name="郵便番号"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="住所"
                    ),
                ),
                (
                    "tel",
                    models.CharField(
                        blank=True, max_length=11, null=True, verbose_name="電話番号"
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="誕生日"),
                ),
                (
                    "business",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="職業"
                    ),
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
    ]
