import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        subprocess.run(["celery", "worker", "--app", "mbq.ranch", "--concurrency", "1"])
