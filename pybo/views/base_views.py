from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from ..models import Article
# l_order_list는 조회순, 추천순 정렬에 사용할 정렬 기준을 저장한 리스트
# 조회순, 추천순 정렬은 Article 모델의 속성을 기준으로 정렬
# 속성 이름 앞에 -를 붙이면 내림차순 정렬
# 속성 이름 앞에 -가 없으면 오름차순 정렬
l_order_list = ('-create_date','-voter','create_date','voter')

# index 함수는 맛집 평가 게시판의 메인 페이지를 출력
def index(request):

    # request.GET.get('page', '1')은 GET 방식으로 요청된 페이지 번호를 의미
    # 즉, 페이지 번호가 없는 경우에는 1을 기본값으로 사용
    page = request.GET.get('page', '1')  # 페이지

    # request.GET.get('l_order', '-create_date')은 GET 방식으로 요청된 정렬 기준을 의미
    # 즉, 정렬 기준이 없는 경우에는 -create_date를 기본값으로 사용
    kw = request.GET.get('kw', '')  # 검색어

    # l_order는 조회순, 추천순 정렬에 사용할 정렬 기준을 저장
    # 조회순, 추천순 정렬은 Article 모델의 속성을 기준으로 정렬
    l_order = request.GET.get('l_order', '-create_date')  # 조회순, 추천순
    
    # l_order가 l_order_list에 포함되어 있지 않으면 l_order를 '-create_date'로 지정
    if l_order not in l_order_list:
        l_order = '-create_date'

    # 조회순, 추천순 정렬
    article_list = Article.objects.order_by(l_order)


    # kw가 있으면 제목, 내용, 질문 글쓴이, 답변 글쓴이를 대상으로 검색
    # Q 객체는 filter 함수의 매칭 조건을 다양하게 설정할 수 있도록 도와주는 클래스
    # Q(subject__icontains=kw)는 subject 속성에 kw가 포함되어 있는지 검사
    # Q(content__icontains=kw)는 content 속성에 kw가 포함되어 있는지 검사
    # Q(author__username__icontains=kw)는 author 속성의 username 속성에 kw가 포함되어 있는지 검사
    # Q(comment__author__username__icontains=kw)는 comment 속성의 author 속성의 username 속성에 kw가 포함되어 있는지 검사
    # icontains는 대소문자를 구분하지 않고 검색
    # contains는 대소문자를 구분하여 검색
    # distinct는 중복을 제거하는 함수
    # 중복을 제거하지 않으면 조회순, 추천순 정렬이 제대로 동작하지 않음

    # 예를 들어, 조회순 정렬을 하면 조회수가 높은 질문이 먼저 출력되어야 하지만
    # 조회수가 높은 질문이 답변이 달린 질문인 경우 답변이 달린 질문이 먼저 출력됨

    # 이때, distinct 함수를 사용하여 중복을 제거하면 답변이 달린 질문이 아닌 조회수가 높은 질문이 먼저 출력됨
    # 즉, distinct 함수를 사용하지 않으면 조회순, 추천순 정렬이 제대로 동작하지 않음
    if kw:
        article_list = article_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(comment__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    # Paginator 클래스는 페이지 기능을 제공하는 클래스
    # Paginator 클래스의 생성자는 2개의 인수를 받음
    # 첫 번째 인수는 전체 데이터 리스트
    # 두 번째 인수는 한 페이지에 보여줄 데이터 개수
    paginator = Paginator(article_list, 10)  # 페이지당 10개씩 보여주기

    # Paginator 클래스의 get_page 메서드는 전달받은 페이지 번호에 해당하는 페이지를 리턴
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj, 'page': page, 'kw': kw, 'l_order': l_order}
    
    # index.html 템플릿에 context 변수를 적용하여 맛집 평가 게시판의 메인 페이지를 출력
    return render(request, 'pybo/article_list.html', context)

# detail 함수는 맛집 평가 게시글의 상세 내용을 출력
# detail 함수는 article_id라는 매개변수를 사용
# article_id는 URL의 끝에 오는 숫자를 article_id라는 변수에 넣어줌
def detail(request, article_id):
    # request.GET.get('page', '1')은 GET 방식으로 요청된 페이지 번호를 의미
    page = request.GET.get('page', '1')  # 페이지

    # request.GET.get('l_order', '-create_date')은 GET 방식으로 요청된 정렬 기준을 의미
    l_order = request.GET.get('l_order', '-create_date')  # 조회순, 추천순

    # l_order가 l_order_list에 포함되어 있지 않으면 l_order를 '-create_date'로 지정
    if l_order not in l_order_list:
        l_order = '-create_date'

    # get_object_or_404 함수는 첫 번째 인수로 모델, 두 번째 인수로 조건을 받음
    # 즉, Article 모델에서 pk가 article_id인 객체를 article 변수에 저장
    # 만약, pk가 article_id인 객체가 존재하지 않으면 오류 메시지를 화면에 출력
    article = get_object_or_404(Article, pk=article_id)

    # 조회수 증가
    article.hits += 1

    # article 모델의 hits 속성에 1을 더한 후 저장
    article.save()

    # 댓글 정렬
    paginator = Paginator(article.comment_set.all().order_by(l_order), 5)

    # Paginator 클래스의 get_page 메서드는 전달받은 페이지 번호에 해당하는 페이지를 리턴
    page_obj = paginator.get_page(page)
    
    # context Dictionary에 article을 저장하여 맛집 평가 게시글 상세 내용 페이지로 전달
    context = {'article': article, 'page_obj': page_obj, 'page': page, 'l_order': l_order, }  
    return render(request, 'pybo/article_detail.html', context)