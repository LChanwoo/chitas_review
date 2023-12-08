from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Article, Comment

@login_required(login_url='common:login')
# comment_create 함수는 답변 등록 기능을 담당
# 답변 등록 기능은 로그인이 필요한 기능이므로 login_required를 사용
def comment_create(request, article_id):

    # article_id는 URL에서 추출한 게시글 번호
    article = get_object_or_404(Article, pk=article_id)
    # request.method는 form 태그의 method 속성에 정의된 값
    if request.method == "POST":
        # request.POST는 POST 요청의 데이터가 저장된 변수
        # 즉, 사용자가 입력한 제목과 내용이 request.POST에 저장됨
        # 이 값을 CommentForm에 전달하여 사용자가 입력한 값을 바탕으로 Comment 모델 객체를 생성
        # CommentForm은 Comment 모델과 연결된 폼
        # CommentForm에 전달된 데이터로 Comment 모델 객체를 생성한 후 데이터베이스에 저장
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.author = request.user
            # comment 모델의 article 속성에 article 변수를 저장
            comment.article = article
            comment.save()
            return redirect('pybo:detail', article_id=article.id)
    else:
        form = CommentForm()
    # context Dictionary에 form을 저장하여 답변 등록 페이지로 전달
    context = {'form': form}
    # comment_form.html 템플릿에 context 변수를 적용하여 답변 등록 페이지를 출력
    # #comment 는 댓글 등록폼을 의미, 그 위치로 이동
    return redirect('{}#comment_{}'.format(
        resolve_url('pybo:detail', article_id=article.id), comment.id))


@login_required(login_url='common:login')
# comment_modify 함수는 답변 수정 기능을 담당
# 답변 수정 기능은 로그인이 필요한 기능이므로 login_required를 사용
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # comment 모델의 author 속성과 로그인 계정이 같은지 확인
    # 즉, 답변을 수정한 사람이 답변 글쓴이와 같은지 확인
    if request.user != comment.author:
        # 다르면 오류 메시지 출력 후 상세 화면으로 이동
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', article_id=comment.article.id)
    
    # request.method는 form 태그의 method 속성에 정의된 값
    # 즉, form 태그의 method 속성이 POST인 경우에만 if문 내부의 코드가 실행
    if request.method == "POST":
        # request.POST는 POST 요청의 데이터가 저장된 변수
        # 즉, 사용자가 입력한 제목과 내용이 request.POST에 저장됨
        # 이 값을 CommentForm에 전달하여 사용자가 입력한 값을 바탕으로 Comment 모델 객체를 생성
        # CommentForm은 Comment 모델과 연결된 폼
        # CommentForm에 전달된 데이터로 Comment 모델 객체를 생성한 후 데이터베이스에 저장
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()

            # 답변 수정이 완료되면 detail 페이지로 이동
            # #comment 는 댓글 등록폼을 의미, 그 위치로 이동
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', article_id=comment.article.id), comment.id))
    else:
        form = CommentForm(instance=comment)

    # context Dictionary에 form을 저장하여 답변 수정 페이지로 전달
    context = {'comment': comment, 'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
# comment_delete 함수는 답변 삭제 기능을 담당
# 답변 삭제 기능은 로그인이 필요한 기능이므로 login_required를 사용
def comment_delete(request, comment_id):

    # comment 모델의 기본 키(id)를 사용하여 삭제할 답변을 가져옴
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # comment 모델의 author 속성과 로그인 계정이 같은지 확인
    if request.user != comment.author:
        # 다르면 오류 메시지 출력 후 상세 화면으로 이동
        messages.error(request, '삭제권한이 없습니다')
    else:
        # 같으면 답변 삭제
        comment.delete()
    # 답변 삭제가 완료되면 detail 페이지로 이동
    return redirect('pybo:detail', article_id=comment.article.id)

@login_required(login_url='common:login')
# comment_vote 함수는 답변 추천 기능을 담당
# 답변 추천 기능은 로그인이 필요한 기능이므로 login_required를 사용
def comment_vote(request, comment_id):
    
    # comment 모델의 기본 키(id)를 사용하여 추천할 답변을 가져옴
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # 본인 답변 추천 방지
    if request.user == comment.author:
        # 오류 메시지 출력 후 상세 화면으로 이동
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        # 추천한 사람 목록(voter)에 현재 유저 추가
        comment.voter.add(request.user)

    # 답변 추천이 완료되면 detail 페이지로 이동
    return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', article_id=comment.article.id), comment.id))
