"""
用戶賬戶模型定義
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    自定義用戶模型
    """
    username = models.CharField(
        '用戶名',
        max_length=30,
        unique=True,
        help_text='必填。30個字符以內。只能包含字母、數字和@/./+/-/_',
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                '用戶名只能包含字母、數字和 @/./+/-/_',
                'invalid'
            ),
        ],
        error_messages={
            'unique': "該用戶名已被使用。",
        },
    )
    
    phone = models.CharField(
        '電話號碼',
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="電話號碼格式：'+886912345678'。"
            )
        ]
    )
    
    birth_date = models.DateField(
        '出生日期',
        null=True,
        blank=True,
        help_text='請選擇您的出生日期'
    )

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = '用戶列表'

    def __str__(self):
        return self.username
