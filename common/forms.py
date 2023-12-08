from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 회원가입 폼
# UserCreationForm은 username, password1, password2를 입력받음
# 이 중 password1은 비밀번호, password2는 비밀번호 확인
# 이 외에 추가적으로 email을 입력받음
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    
    # Meta 클래스는 UserForm 클래스 내부에 중첩 클래스로 정의
    # UserForm 클래스에 대한 추가적인 정보를 정의하는 내부 클래스
    # model = User는 이 폼을 사용해서 User 모델을 저장한다는 의미
    # fields = ("username", "password1", "password2", "email")는
    # 이 폼에 username, password1, password2, email 필드가 있음을 의미
    # UserCreationForm은 username, password1, password2를 이미 내부적으로 정의하고 있음
    # 따라서 email 필드만 추가로 정의해주면 됨
    # 이때 UserCreationForm에 이미 정의된 필드의 순서를 변경하고 싶다면
    # fields = ("email", "username", "password1", "password2")와 같이 순서를 변경
    # 필드 이름은 User 모델의 속성 이름과 일치해야 함
    # User 모델의 속성 이름은 username, password, email 등임
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")