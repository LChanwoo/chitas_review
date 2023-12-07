from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import ArticleForm
from ..models import Article

@login_required(login_url='common:login')
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # author 속성에 로그인 계정 저장
            article.create_date = timezone.now()
            article.save()
            return redirect('pybo:index')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'pybo/article_form.html', context)

@login_required(login_url='common:login')
def article_modify(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', article_id=article.id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.modify_date = timezone.now()  # 수정일시 저장
            article.save()
            return redirect('pybo:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'pybo/article_form.html', context)

@login_required(login_url='common:login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', article_id=article.id)
    article.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def article_vote(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        article.voter.add(request.user)
    return redirect('pybo:detail', article_id=article.id)
