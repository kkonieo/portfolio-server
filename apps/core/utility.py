import os
import uuid


def get_uuid_path(instance, filename: str) -> str:
    """
    파일이름 앞 uuid를 추가한다.
    """
    uuid4 = uuid.uuid4()
    new_path = os.path.join("upload/", f"{uuid4}_{filename}")
    return new_path
