"""
主項目URL配置
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("polls.urls")),  # 首頁使用問卷列表
    path("polls/", include("polls.urls")),  # 問卷相關URL
    path("accounts/", include("accounts.urls")),  # 用戶認證相關URL
    path("admin/", admin.site.urls),  # 管理後台
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)