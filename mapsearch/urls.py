from django.urls import include, path
from . import views #views.py import


urlpatterns = [
    path('keyword', views.keyword, name='keyword'),
]