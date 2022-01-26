import os
import random
import string
import uuid
from typing import List


def get_uuid_path(instance, filename: str) -> str:
    """
    파일이름 앞 uuid를 추가한다.
    """
    uuid4 = uuid.uuid4()
    new_path = os.path.join("upload/", f"{uuid4}_{filename}")
    return new_path


def generate_random_string(
    length: int = 10, chars: List[str] = string.ascii_lowercase + string.digits
) -> str:
    """
    랜덤 문자열 생성
    """
    return "".join([random.choice(chars) for _ in range(length)])
