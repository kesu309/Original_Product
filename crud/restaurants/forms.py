from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant, Review, Reservation, Profile
from django.utils import timezone
from datetime import datetime, time, timedelta
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='必須。有効なメールアドレスを入力してください。')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 日本語化
        self.fields['username'].label = 'ユーザー名'
        self.fields['email'].label = 'メールアドレス'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認）'

class RestaurantSearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '店舗名、カテゴリー、エリアで検索'
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username_kana', 'post_code', 'address', 'tel', 'birth_date', 'business']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        } 