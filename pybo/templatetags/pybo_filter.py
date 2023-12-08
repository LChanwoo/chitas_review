import markdown
from django import template
from django.utils.safestring import mark_safe

# 템플릿 필터를 만들 때는 함수를 정의한 후, register.filter 함수의 인수로 함수를 등록
# 이때, 함수의 이름이 템플릿 필터의 이름이 됨
# 템플릿에서 사용할 때는 {{ value|sub:arg }}와 같이 사용
# value는 필터를 적용할 값이고, arg는 필터에 전달할 인수
# 여기서는 value에서 arg를 뺀 값을 반환하는 필터를 만듦
# 템플릿 필터를 만들 때는 함수의 인수로 value 외에 추가로 최대 2개까지 인수를 받을 수 있음
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    
    # markdown.markdown 함수를 사용하여 value를 HTML로 변환
    # 이때, markdown.markdown 함수의 extensions 인수에 'nl2br'과 'fenced_code'를 지정
    # nl2br은 줄바꿈 문자를 <br> 태그로 변환하고, fenced_code는 코드 블록을 쉽게 입력할 수 있도록 함
    # 이렇게 변환된 HTML은 mark_safe 함수로 감싸서 반환

    # mark_safe 함수로 감싸지 않으면 HTML이 escape되어 템플릿에 표시되지 않음
    # mark_safe 함수는 HTML이 안전하다는 것을 알려주는 함수
    # 이 함수를 사용하지 않으면 HTML이 escape되어 템플릿에 표시되지 않음
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))