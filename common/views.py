from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

# 회원가입
def signup(request):
    # POST 방식으로 요청이 들어온 경우
    # 즉, 회원가입 정보를 입력하고 가입하기 버튼을 누른 경우
    # 회원가입 정보를 바탕으로 회원을 생성한 후 로그인 처리
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    # GET 방식으로 요청이 들어온 경우
    # 즉, 회원가입 페이지를 최초로 요청하는 경우
    # 빈 회원가입 폼을 보여줌
    # 사용자가 회원가입 정보를 입력하고 가입하기 버튼을 누르면
    # 이후에는 POST 방식으로 요청이 들어오게 됨
    else:
        form = UserForm()
    
    # GET 방식으로 요청이 들어오거나
    # POST 방식으로 요청이 들어와도 유효성 검증에 실패한 경우
    # 즉, 회원가입 정보를 입력하고 가입하기 버튼을 눌렀는데
    # 아이디나 비밀번호가 너무 짧은 경우
    # 회원가입 폼에 에러 메시지를 같이 보여줌
    # 이때, 에러 메시지는 UserForm 클래스에서 정의한 에러 메시지가 아닌
    # User 모델에서 정의한 에러 메시지가 보여짐
    return render(request, 'common/signup.html', {'form': form})