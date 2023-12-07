from django.contrib import admin
from django.urls import path, include # include 추가
from pybo.views import base_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pybo.urls')), # pybo/urls.py 추가
    path('common/', include('common.urls')), # common/urls.py 추가
    path('/', base_views.index, name='index'),
    path('mapsearch/', include('mapsearch.urls')),
]
