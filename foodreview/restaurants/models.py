from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)

class Review(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE,
        related_name='restaurant_reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='restaurant_user_reviews'
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}"
