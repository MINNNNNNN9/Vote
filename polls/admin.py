"""
問卷調查應用的管理界面配置
"""

from django.contrib import admin
from .models import Question, Choice, Vote

class ChoiceInline(admin.TabularInline):
    """在問題編輯頁面內聯顯示選項"""
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """問題管理界面配置"""
    fieldsets = [
        (None, {"fields": ["question_text", "type"]}),
        ("日期信息", {"fields": ["pub_date"]}),
        ("顯示設置", {"fields": ["position", "is_active"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "is_active"]
    list_filter = ["pub_date", "is_active"]
    search_fields = ["question_text"]
    ordering = ["position", "-pub_date"]

class VoteAdmin(admin.ModelAdmin):
    """投票記錄管理界面配置"""
    list_display = ['user', 'question', 'choice', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'question__question_text']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)