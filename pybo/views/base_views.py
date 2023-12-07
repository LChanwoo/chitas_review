from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Article

l_order_list = ('-create_date','-voter','create_date','voter')

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    l_order = request.GET.get('l_order', '-create_date')  # 조회순, 추천순
    if l_order not in l_order_list:
        l_order = '-create_date'
    # 조회순, 추천순 정렬
    article_list = Article.objects.order_by(l_order)
    if kw:
        article_list = article_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(comment__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(article_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj, 'page': page, 'kw': kw, 'l_order': l_order}
    return render(request, 'pybo/article_list.html', context)

def detail(request, article_id):
    page = request.GET.get('page', '1')  # 페이지
    l_order = request.GET.get('l_order', '-create_date')  # 조회순, 추천순
    if l_order not in l_order_list:
        l_order = '-create_date'
    article = get_object_or_404(Article, pk=article_id)
    article.hits += 1
    article.save()
    print(l_order)
    paginator = Paginator(article.comment_set.all().order_by(l_order), 5)
    page_obj = paginator.get_page(page)
    context = {'article': article, 'page_obj': page_obj, 'page': page, 'l_order': l_order }  
    return render(request, 'pybo/article_detail.html', context)