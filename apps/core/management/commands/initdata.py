import os
from glob import glob

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "미리 정의된 기본 데이터를 추가합니다."

    def handle(self, *args, **options):

        # fixture 디렉터리 경로
        fixture_directory = os.path.join(settings.BASE_DIR, "fixtures")

        # fixtrue 디렉터리가 존재하는지 체크
        if not os.path.isdir(fixture_directory):
            raise FileNotFoundError(f"{fixture_directory} 디렉터리가 존재하지 않습니다.")

        # json 파일만 가져온다
        files = glob(f"{fixture_directory}/*.json")
        for file in files:
            management.call_command("loaddata", file)
