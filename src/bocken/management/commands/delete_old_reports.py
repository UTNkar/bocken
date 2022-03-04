from django.core.management.base import BaseCommand
from bocken.models import Report


class Command(BaseCommand):  # noqa
    help = 'Delete old reports'

    def handle(self, *args, **options):  # noqa
        Report.delete_old_reports()
