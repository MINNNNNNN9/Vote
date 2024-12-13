"""
問卷調查應用的視圖定義。
包含問卷列表、詳情、結果展示等功能。
"""

from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Choice, Question, Vote

class IndexView(generic.ListView):
    """
    問卷列表視圖
    顯示最近發布的問卷列表，支持分頁
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 10  # 每頁顯示10個問題

    def get_queryset(self):
        """
        獲取已發布的問卷列表，按發布時間倒序排序
        排除未來發布的問卷
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            is_active=True
        ).order_by("-pub_date", "position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_questions'] = Question.objects.count()
        context['active_questions'] = Question.objects.filter(is_active=True).count()
        return context

class DetailView(LoginRequiredMixin, generic.DetailView):
    """
    問卷詳情視圖
    顯示單個問卷的詳細信息和投票選項
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        確保只能查看已發布的問卷
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choices.all()
        if self.request.user.is_authenticated:
            try:
                user_vote = Vote.objects.get(
                    user=self.request.user,
                    question=self.object
                )
                context['user_previous_vote'] = user_vote.choice
            except Vote.DoesNotExist:
                context['user_previous_vote'] = None
        return context

class ResultsView(generic.DetailView):
    """
    問卷結果視圖
    顯示問卷的投票結果統計
    """
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 計算總投票數
        total_votes = sum(choice.votes for choice in self.object.choices.all())
        choices = self.object.choices.all()
        
        # 為每個選項計算百分比
        for choice in choices:
            choice.percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
            
        context['choices'] = choices
        context['total_votes'] = total_votes
        return context

@login_required
@transaction.atomic
def vote(request, question_id):
    """
    處理投票請求
    
    Args:
        request: HTTP請求對象
        question_id: 問題ID
    
    Returns:
        HttpResponse: 重定向到結果頁面或重新顯示投票表單
    """
    question = get_object_or_404(Question, pk=question_id)
    
    if not question.is_active:
        messages.error(request, "這個問卷已經關閉，無法投票。")
        return HttpResponseRedirect(reverse("polls:index"))
    
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新顯示投票表單
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "你沒有選擇任何選項。",
        })

    try:
        # 檢查用戶是否已經投過票
        vote_record = Vote.objects.get(user=request.user, question=question)
        # 如果已投票，更新選擇並調整計數
        if vote_record.choice != selected_choice:
            with transaction.atomic():
                vote_record.choice.votes -= 1  # 減少原來選項的票數
                vote_record.choice.save()
                selected_choice.votes += 1  # 增加新選項的票數
                selected_choice.save()
                vote_record.choice = selected_choice  # 更新用戶的選擇
                vote_record.save()
                messages.success(request, '你已成功更改投票！')
        else:
            messages.info(request, '你已經投過這個選項了。')
    except Vote.DoesNotExist:
        # 如果是首次投票
        with transaction.atomic():
            selected_choice.votes += 1
            selected_choice.save()
            Vote.objects.create(
                user=request.user,
                question=question,
                choice=selected_choice
            )
            messages.success(request, '投票成功！')

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))