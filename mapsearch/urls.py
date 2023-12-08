from django.urls import include, path
from . import views #views.py import


urlpatterns = [
    # 카카오 지도 검색
    # /mapsearch/로 시작하는 URL은 mapsearch/urls.py 파일에서 처리
    # keyword를 이용하여 검색한 결과를 반환하는 api 
    path('keyword', views.keyword, name='keyword'),
]