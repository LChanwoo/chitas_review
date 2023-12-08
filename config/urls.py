from django.contrib import admin
from django.urls import path, include # include 추가
from pybo.views import base_views

urlpatterns = [
    # admin 페이지는 /admin/으로 시작하는 URL이 처리
    path('admin/', admin.site.urls),
    # ''로 시작하는 URL은 모두 pybo/urls.py 파일에서 처리
    path('', include('pybo.urls')), # pybo/urls.py 추가
    # 로그인, 회원가입 관련 URL은 common/urls.py 파일에서 처리 
    path('common/', include('common.urls')), # common/urls.py 추가
    # 인덱스 페이지는 base_views.py 파일의 index 함수에서 처리
    path('/', base_views.index, name='index'),
    # 카카오 지도 검색 관련 URL은 mapsearch/urls.py 파일에서 처리
    path('mapsearch/', include('mapsearch.urls')),
]
