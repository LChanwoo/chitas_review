from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_article')
    subject = models.CharField(max_length=200) # 제목
    content = models.TextField() # 내용
    create_date = models.DateTimeField() # 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_article')  # 추천인 추가
    locate_x = models.FloatField(null=False, default=0) # x 좌표 추가
    locate_y = models.FloatField(null=False, default=0) # y 좌표 추가
    zeropay = models.BooleanField(default=False)
    place_name = models.CharField(max_length=200, default='') # 상호명 추가
    phone = models.CharField(max_length=200, default='') # 전화번호 추가
    road_address_name = models.CharField(max_length=200, default='') # 주소 추가
    hits = models.PositiveIntegerField(default=0) # 조회수 추가

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 질문
    content = models.TextField() # 내용
    create_date = models.DateTimeField() # 작성일시
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일시
    voter = models.ManyToManyField(User, related_name='voter_comment')
