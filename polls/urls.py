"""
問卷調查應用的URL配置。
定義了所有的路由映射關係。
"""

from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # 問卷列表頁
    path("", 
         views.IndexView.as_view(), 
         name="index"),
    
    # 問卷詳情頁
    path("<int:pk>/", 
         views.DetailView.as_view(), 
         name="detail"),
    
    # 投票結果頁
    path("<int:pk>/results/", 
         views.ResultsView.as_view(), 
         name="results"),
    
    # 投票處理
    path("<int:question_id>/vote/", 
         views.vote, 
         name="vote"),
]