from django_cron import CronJobBase, Schedule
from .models import Report, Agreement


class DeleteOldReportsCronJob(CronJobBase):
    """Cron job for deleting old reports."""

    RUN_AT_TIMES = ['0:30']
    DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 60

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'bocken.delete_old_reports'

    def do(self):  # noqa
        Report.delete_older_than_one_year()


class AutomaticRenewalReminder(CronJobBase):
    """Cron job for deleting old reports."""

    RUN_AT_TIMES = ['12:30']
    DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 60

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'bocken.automatic_renewal_reminder'

    def do(self):  # noqa
        Agreement.send_renewal_reminder_10_days_left()
