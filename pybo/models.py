from django.db import models
from django.contrib.auth.models import User

# Article 모델은 맛집 정보와 유저의 평가를 저장하는 모델
# Article 모델은 User 모델과 1:N 관계를 가짐
# 즉, 하나의 유저는 여러 개의 맛집 정보를 등록할 수 있음
class Article(models.Model):
    
    # 작성자 정보를 저장하기 위해 User 모델과 1:N 관계를 가짐
    # on_delete=models.CASCADE는 User 모델이 삭제되면 연결된 질문도 함께 삭제됨을 의미
    # related_name='author_article'는 User 모델이 연결된 질문을 쉽게 가져올 수 있도록
    # 연결된 질문에 대한 역참조를 author_article로 지정
    # 즉, User 모델은 author_article 속성을 통해 연결된 질문을 가져올 수 있음
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_article')
    
    # 제목은 최대 200자까지 입력 가능
    subject = models.CharField(max_length=200) # 제목
    
    # 내용은 TextField로 제한 없이 입력 가능
    content = models.TextField() # 내용
    
    # 작성일시는 DateTimeField로 날짜와 시간을 저장
    create_date = models.DateTimeField() # 작성일시
    
    # 수정일시는 DateTimeField로 날짜와 시간을 저장
    # 수정일시는 수정하지 않아도 되므로 null=True, blank=True로 지정
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일시
    
    # 추천인은 ManyToManyField로 다대다 관계를 의미
    # 1개의 질문에 여러 명의 추천인이 있을 수 있고
    # 1명의 추천인은 여러 개의 질문을 추천할 수 있음
    # 따라서 ManyToManyField를 사용하여 다대다 관계를 만듦
    # related_name='voter_article'는 질문이 연결된 추천인을 쉽게 가져올 수 있도록 연결된 추천인에 대한 역참조를 voter_article로 지정
    # 즉, 질문은 voter_article 속성을 통해 연결된 추천인을 가져올 수 있음
    voter = models.ManyToManyField(User, related_name='voter_article')  # 추천인 추가
    
    # 가게 위치를 위한 x,y 좌표
    locate_x = models.FloatField(null=False, default=0) # x 좌표 추가
    locate_y = models.FloatField(null=False, default=0) # y 좌표 추가
    
    # 제로페이 사용 여부, 기본값은 False (사용안함)
    zeropay = models.BooleanField(default=False)
    
    # 상호명, 전화번호, 주소 정보 추가
    place_name = models.CharField(max_length=200, default='') # 상호명 추가
    phone = models.CharField(max_length=200, default='') # 전화번호 추가
    road_address_name = models.CharField(max_length=200, default='') # 주소 추가
    
    # 조회수 추가
    hits = models.PositiveIntegerField(default=0) # 조회수 추가

# Comment 모델은 맛집 정보에 대한 유저의 평가를 저장하는 모델
# Comment 모델은 User 모델과 1:N 관계를 가짐
# 즉, 하나의 유저는 여러 개의 맛집 정보에 대한 평가를 남길 수 있음
class Comment(models.Model):
    # 작성자 정보를 저장하기 위해 User 모델과 1:N 관계를 가짐
    # on_delete=models.CASCADE는 User 모델이 삭제되면 연결된 답변도 함께 삭제됨을 의미
    # related_name='author_comment'는 User 모델이 연결된 답변을 쉽게 가져올 수 있도록
    # 연결된 답변에 대한 역참조를 author_comment로 지정
    # 즉, User 모델은 author_comment 속성을 통해 연결된 답변을 가져올 수 있음
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    
    # 답변이 연결된 질문은 답변이 삭제되면 질문도 함께 삭제됨
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 질문

    # 내용은 TextField로 제한 없이 입력 가능
    content = models.TextField() # 내용

    # 작성일시는 DateTimeField로 날짜와 시간을 저장
    create_date = models.DateTimeField() # 작성일시

    # 수정일시는 DateTimeField로 날짜와 시간을 저장
    # 수정일시는 수정하지 않아도 되므로 null=True, blank=True로 지정
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일시

    # related_name='voter_comment'는 답변이 연결된 추천인을 쉽게 가져올 수 있도록
    # 연결된 추천인에 대한 역참조를 voter_comment로 지정
    voter = models.ManyToManyField(User, related_name='voter_comment')
