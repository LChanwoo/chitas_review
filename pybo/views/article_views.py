from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import ArticleForm
from ..models import Article

# @login_required(login_url='common:login')
# @login_required는 로그인이 필요한 기능에 사용
# 로그인이 되어 있지 않으면 로그인 페이지로 이동
# 로그인 페이지는 common/urls.py에 정의되어 있음
# @는 데코레이터라고 부르며, 함수를 꾸며주는 역할

@login_required(login_url='common:login')
# article_create 함수는 맛집 평가 게시글 등록 기능을 담당
# 맛집 평가 게시글 등록 기능은 로그인이 필요한 기능이므로 login_required를 사용
# 로그인이 되어 있지 않으면 로그인 페이지로 이동
def article_create(request):
    
    # request.method는 form 태그의 method 속성에 정의된 값
    # 즉, form 태그의 method 속성이 POST인 경우에만 if문 내부의 코드가 실행
    # form 태그의 method 속성이 GET인 경우에는 else문 내부의 코드가 실행
    # form 태그의 method 속성은 생략 가능
    # 생략할 경우, method 속성의 기본값은 GET
    if request.method == 'POST':

        # request.POST는 POST 요청의 데이터가 저장된 변수
        # 즉, 사용자가 입력한 제목과 내용이 request.POST에 저장됨
        # 이 값을 ArticleForm에 전달하여 사용자가 입력한 값을 바탕으로 Article 모델 객체를 생성
        # ArticleForm은 Article 모델과 연결된 폼
        # ArticleForm에는 Article 모델의 각 속성에 대한 입력 필드가 있음
        form = ArticleForm(request.POST)

        if form.is_valid():

            # form.save() 함수는 ArticleForm에 전달된 데이터로 Article 모델 객체를 생성한 후 데이터베이스에 저장
            # commit=False는 임시 저장을 의미
            # 즉, 데이터베이스에 저장하지 않고 메모리 상에만 객체를 만들어 줌
            # 이후, article.author = request.user와 같이 author 속성에 로그인 계정을 저장
            # 그리고 article.create_date = timezone.now()와 같이 작성일시를 저장
            # 마지막으로 article.save() 함수를 호출하여 데이터베이스에 저장
            # 이때, article.author와 article.create_date는 ArticleForm에 정의되지 않은 속성
            article = form.save(commit=False)
            article.author = request.user  # author 속성에 로그인 계정 저장
            article.create_date = timezone.now()
            article.save()
            
            # redirect 함수는 인수로 지정된 URL로 이동
            # 저장이 완료되면 redirect 함수를 호출하여 메인 페이지로 이동
            return redirect('pybo:index')
    else:
        # request.method가 POST가 아닌 경우
        # 즉, 맛집 평가 게시글 등록 페이지를 최초로 요청하는 경우
        # ArticleForm을 생성하여 form 변수에 저장
        # 이때, ArticleForm의 생성자에 아무런 값도 전달하지 않았으므로
        # 사용자 입력 필드는 빈 상태로 생성됨
        form = ArticleForm()

    # context Dictionary에 form을 저장하여 맛집 평가 게시글 등록 페이지로 전달
    context = {'form': form}

    # render 함수는 context에 있는 데이터를 사용하여 'pybo/article_form.html' 템플릿 파일을 HTML로 변환
    # 이후, 변환된 HTML을 사용자에게 전달
    return render(request, 'pybo/article_form.html', context)

@login_required(login_url='common:login')
# article_modify 함수는 맛집 평가 게시글 수정 기능을 담당
# 맛집 평가 게시글 수정 기능은 로그인이 필요한 기능이므로 login_required를 사용
# 로그인이 되어 있지 않으면 로그인 페이지로 이동
# article_modify 함수는 article_id라는 매개변수를 사용
# article_id는 URL의 끝에 오는 숫자를 article_id라는 변수에 넣어줌
# 예를 들어, /pybo/3/이라는 URL은 article_id에 3이라는 값이 저장됨
# 이렇게 저장된 값을 detail 함수의 매개변수로 넘겨줌
def article_modify(request, article_id):
    
    # Article 모델의 기본 키(id)를 사용하여 수정할 게시글을 가져옴
    # 이때, 게시글이 존재하지 않으면 오류 메시지를 화면에 출력
    article = get_object_or_404(Article, pk=article_id)

    # 수정하려는 게시글의 작성자와 로그인 계정이 다른 경우 오류 메시지를 화면에 출력
    # 이때, 로그인 계정은 request.user에 저장되어 있음
    # 즉, request.user와 article.author가 같은지 비교
    if request.user != article.author:

        # 같지 않으면 오류 메시지를 화면에 출력
        messages.error(request, '수정권한이 없습니다')
        
        # 오류 메시지와 함께 detail 페이지로 이동
        return redirect('pybo:detail', article_id=article.id)
    
    # request.method는 form 태그의 method 속성에 정의된 값
    # 즉, form 태그의 method 속성이 POST인 경우에만 if문 내부의 코드가 실행
    # form 태그의 method 속성이 GET인 경우에는 else문 내부의 코드가 실행
    if request.method == "POST":

        # request.POST는 POST 요청의 데이터가 저장된 변수
        form = ArticleForm(request.POST, instance=article)

        # form.save() 함수는 ArticleForm에 전달된 데이터로 Article 모델 객체를 생성한 후 데이터베이스에 저장
        if form.is_valid():

            # commit=False는 임시 저장을 의미
            article = form.save(commit=False)
            article.modify_date = timezone.now()  # 수정일시 저장
            article.save()

            # 게시글 수정이 완료되면 detail 페이지로 이동
            return redirect('pybo:detail', article_id=article.id)
    else:
        # 맛집 평가 게시글 수정 페이지를 최초로 요청하는 경우
        # ArticleForm을 생성하여 form 변수에 저장
        # 이때, ArticleForm의 생성자에 아무런 값도 전달하지 않았으므로
        # 사용자 입력 필드는 article 객체의 값으로 채워진 상태로 생성됨
        # 즉, 사용자가 입력하지 않은 필드는 article 객체의 값으로 채워짐
        # 사용자가 입력하지 않은 필드는 article 객체의 값으로 채워지므로 사용자가 입력하지 않은 필드는 수정되지 않음
        form = ArticleForm(instance=article)

    # context Dictionary에 form을 저장하여 맛집 평가 게시글 수정 페이지로 전달
    # 이때, form에는 article 객체의 값이 저장되어 있으므로 사용자가 수정할 수 있음
    context = {'form': form}
    return render(request, 'pybo/article_form.html', context)

@login_required(login_url='common:login')
# article_delete 함수는 맛집 평가 게시글 삭제 기능을 담당
def article_delete(request, article_id):

    # Article 모델의 기본 키(id)를 사용하여 삭제할 게시글을 가져옴
    article = get_object_or_404(Article, pk=article_id)

    # 삭제하려는 게시글의 작성자와 로그인 계정이 다른 경우 오류 메시지를 화면에 출력
    if request.user != article.author:
        # 오류 메시지와 함께 detail 페이지로 이동
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', article_id=article.id)
    
    # 게시글 삭제는 POST 방식으로만 처리
    # GET 방식으로 요청이 들어오면 오류 메시지를 화면에 출력
    article.delete()
    # 게시글 삭제가 완료되면 메인 페이지로 이동
    return redirect('pybo:index')

@login_required(login_url='common:login')
# article_vote 함수는 맛집 평가 게시글 추천 기능을 담당
def article_vote(request, article_id):

    # Article 모델의 기본 키(id)를 사용하여 추천할 게시글을 가져옴
    article = get_object_or_404(Article, pk=article_id)

    # 본인이 작성한 글은 추천할 수 없음
    if request.user == article.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
        
    # 본인이 작성한 글이 아닌 경우 추천 기능을 수행
    else:
        article.voter.add(request.user)

    # 추천 기능이 완료되면 detail 페이지로 이동
    return redirect('pybo:detail', article_id=article.id)
