"""
用戶賬戶表單定義
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    """
    用戶註冊表單
    """
    email = forms.EmailField(
        label='電子郵件',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    birth_date = forms.DateField(
        label='出生日期',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat()
            }
        )
    )
    
    phone = forms.CharField(
        label='電話號碼',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '+886912345678'
            }
        )
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入3-30個字符'
            }),
        }
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError('出生日期不能晚於今天')
        return birth_date
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('該電子郵件已被註冊')
        return email

class CustomUserChangeForm(UserChangeForm):
    """
    用戶信息修改表單
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'max': date.today().isoformat()
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+886912345678'
                }
            )
        }
