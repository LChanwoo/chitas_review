from django import forms
from pybo.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # 사용할 모델
        fields = ['place_name','phone','road_address_name' ,'subject', 'content', 'locate_x', 'locate_y', 'zeropay' ]  # ArticleForm에서 사용할 Article 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
            'locate_x': 'x좌표',
            'locate_y': 'y좌표',
            'zeropay': '제로페이 사용',
            'place_name':'상호명',
            'phone':'전화번호',
            'road_address_name':'주소',
        } 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }