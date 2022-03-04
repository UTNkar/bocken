from django.core.management.base import BaseCommand
from bocken.models import Agreement

class Command(BaseCommand):
    help = 'Send automatic renewal reminders'

    def handle(self, *args, **options):
        Agreement.send_renewal_reminder_10_days_left()
