from django import template
from ..models import Favorite

register = template.Library()

@register.filter
def is_favorited(restaurant_id, user):
    """
    レストランがユーザーによってお気に入り登録されているかを確認します
    """
    if user.is_authenticated:
        return Favorite.objects.filter(restaurant_id=restaurant_id, user=user).exists()
    return False 