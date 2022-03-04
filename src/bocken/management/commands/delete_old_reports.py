from django.core.management.base import BaseCommand
from bocken.models import Report

class Command(BaseCommand):
    help = 'Delete old reports'

    def handle(self, *args, **options):
        Report.delete_old_reports()
