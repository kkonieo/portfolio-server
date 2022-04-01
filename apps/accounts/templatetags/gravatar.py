import hashlib
from django import template

# 기존 템플릿 라이브러리에 새로운 템플릿 추가
register = template.Library()

# 아래 함수를 필터로 등록
@register.filter
def makemd5(email):
    return hashlib.md5(email.encode('utf-8').lower().strip()).hexdigest()