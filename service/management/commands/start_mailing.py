import logging

from django.core.management.base import BaseCommand

from service.services import run_apscheduler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        run_apscheduler()
