from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'area', 'opening_time', 'closing_time')
    list_filter = ('category', 'area')
    search_fields = ('name',)
    ordering = ('name',)
