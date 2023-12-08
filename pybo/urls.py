from django.urls import path
from .views import base_views, article_views, comment_views
app_name = 'pybo'

# views 파일을 base_views.py, article_views.py, comment_views.py로 분리
# 각각의 파일에는 뷰 함수를 작성
# 이렇게 하면 코드가 길어지는 것을 방지할 수 있음
# 또한, 코드를 분리하면 코드를 수정할 때도 편리함

urlpatterns = [
    
     # base_views.py
     path('', base_views.index, name='index'),
     # <int:article_id>는 URL의 끝에 오는 숫자를 article_id라는 변수에 넣어줌
     # 예를 들어, /pybo/3/이라는 URL은 article_id에 3이라는 값이 저장됨
     # 이렇게 저장된 값을 detail 함수의 매개변수로 넘겨줌
     # detail 함수는 article_id에 해당하는 질문을 찾아서 보여줌
     # name='detail'은 URL 패턴의 이름을 detail로 지정
     # 이렇게 하면 템플릿 파일에서 {% url 'pybo:detail' article.id %}와 같이 사용 가능
     path('<int:article_id>/', base_views.detail, name='detail'),

     # article_views.py
     path('article/create/', article_views.article_create, name='article_create'),
     path('article/modify/<int:article_id>/', article_views.article_modify, name='article_modify'),
     path('article/delete/<int:article_id>/', article_views.article_delete, name='article_delete'),
     path('article/vote/<int:article_id>/', article_views.article_vote, name='article_vote'),

     # comment_views.py
     path('comment/create/<int:article_id>/', comment_views.comment_create, name='comment_create'),
     path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
     path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),
     path('comment/vote/<int:comment_id>/', comment_views.comment_vote, name='comment_vote'),
]
