from django_cron import CronJobBase, Schedule
from .models import Report


class DeleteOldReportsCronJob(CronJobBase):
    """Cron job for deleting old reports."""

    RUN_AT_TIMES = ['0:30']
    DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 60

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'bocken.delete_old_reports'

    def do(self):  # noqa
        Report.delete_old_reports()
