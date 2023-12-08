from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app 이름을 common으로 지정했으므로
# URL 패턴의 이름은 common:login, common:logout, common:signup이 됨

# 이 URL 패턴의 이름은 템플릿 파일에서 사용됨
# 예를 들어, 로그인 링크를 만들 때 {% url 'common:login' %}과 같이 사용
# 이렇게 하면 URL 패턴의 이름이 변경되어도 템플릿 파일을 수정할 필요가 없음

# 또한, URL 패턴의 이름을 사용하면 URL 패턴이 변경되어도
# URL 패턴의 이름이 사용된 뷰 함수는 수정할 필요가 없음

# URL 패턴의 이름은 config/urls.py 파일에서 app_name 변수에 지정
# app_name 변수에 지정한 이름은 config/urls.py 파일에서 include 함수에 사용
# 예를 들어, include('common.urls')와 같이 사용
app_name = 'common'

urlpatterns = [

    # 로그인 폼 템플릿은 /template/common/login.html을 사용
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 회원가입 폼 템플릿은 /template/common/signup.html을 사용
    path('signup/', views.signup, name='signup'),
]