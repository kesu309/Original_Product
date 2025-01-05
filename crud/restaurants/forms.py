from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant, Review, Reservation, Profile
from django.utils import timezone
from datetime import datetime, time, timedelta

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
        label='キーワード',
        widget=forms.TextInput(attrs={
            'placeholder': '店舗名、カテゴリ、エリアで検索',
            'class': 'search-input'
        })
    ) 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{'★' * i}") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'レビューを書く'})
        }

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 30分刻みの時間選択肢を生成
        time_choices = []
        start = time(11, 0)  # 11:00から
        end = time(20, 30)   # 20:30まで
        current = datetime.combine(datetime.today(), start)
        while current.time() <= end:
            t = current.time()
            time_choices.append((
                t.strftime('%H:%M'),
                t.strftime('%H:%M')
            ))
            current += timedelta(minutes=30)
        
        self.fields['time'] = forms.ChoiceField(
            choices=time_choices,
            label='予約時間',
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'number_of_people': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control'
            })
        }
        labels = {
            'date': '予約日',
            'number_of_people': '人数',
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_str = cleaned_data.get('time')
        
        if date and time_str:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            if date < timezone.now().date():
                raise forms.ValidationError('過去の日付は選択できません。')
            elif date == timezone.now().date() and time_obj < timezone.now().time():
                raise forms.ValidationError('過去の時間は選択できません。')
        
        return cleaned_data 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username_kana', 'post_code', 'address', 'tel']
        labels = {
            'username_kana': 'フリガナ',
            'post_code': '郵便番号',
            'address': '住所',
            'tel': '電話番号',
        } 