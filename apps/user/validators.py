from django.core import validators
from django.utils.translation import gettext_lazy as _


class NameValidator(validators.RegexValidator):
    # 한글만 입력 가능
    regex = r"^[가-힣]+\Z"
    message = "올바른 이름을 입력해주세요. (한글)"
    flags = 0
