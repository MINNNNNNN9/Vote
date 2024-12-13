"""
問卷調查應用的模型定義。
包含問卷和選項兩個主要模型。
"""

from django.db import models
from django.utils import timezone
from django.conf import settings

class Question(models.Model):
    """問卷模型"""
    
    TYPE_CHOICES = [
        ('single', '單選題'),
        ('multiple', '多選題'),
    ]
    
    question_text = models.CharField('問題內容', max_length=200)
    pub_date = models.DateTimeField('發布時間', default=timezone.now)
    type = models.CharField('題目類型', max_length=8, choices=TYPE_CHOICES, default='single')
    position = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否啟用', default=True)

    class Meta:
        verbose_name = '問卷'
        verbose_name_plural = '問卷列表'
        ordering = ['position', '-pub_date']

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    """選項模型"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='所屬問題'
    )
    choice_text = models.CharField('選項內容', max_length=200)
    votes = models.IntegerField('得票數', default=0)

    class Meta:
        verbose_name = '選項'
        verbose_name_plural = '選項列表'

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    """投票記錄模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='投票用戶'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='投票問題'
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name='選擇選項'
    )
    created_at = models.DateTimeField('投票時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '投票記錄'
        verbose_name_plural = '投票記錄列表'
        # 確保每個用戶對每個問題只能投一次票
        unique_together = ['user', 'question']

    def __str__(self):
        return f'{self.user.username} - {self.question.question_text} - {self.choice.choice_text}'