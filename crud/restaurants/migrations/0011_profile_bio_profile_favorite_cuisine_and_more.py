# Generated by Django 5.1.4 on 2025-01-27 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0010_reservation_reservation_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, verbose_name="自己紹介"),
        ),
        migrations.AddField(
            model_name="profile",
            name="favorite_cuisine",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="好きな料理"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="nickname",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="ニックネーム"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="address",
            field=models.CharField(default="", max_length=200, verbose_name="住所"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="post_code",
            field=models.CharField(default="", max_length=7, verbose_name="郵便番号"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="tel",
            field=models.CharField(default="", max_length=11, verbose_name="電話番号"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="username_kana",
            field=models.CharField(default="", max_length=100, verbose_name="フリガナ"),
        ),
    ]
