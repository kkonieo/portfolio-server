from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "기본 기술스택 데이터를 추가합니다."

    def handle(self, *args, **options):
        management.call_command("loaddata", "skills")
