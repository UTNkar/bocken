from django.db import models
from django.utils.translation import gettext_lazy as _
from . import JournalEntry


class Report(models.Model):
    """
    A report is a collection of journal entries.

    A report is created by adnministrators and shows how much each group has
    driven bocken between the first and last journal entry of a report
    """

    first = models.ForeignKey(
        "JournalEntry",
        on_delete=models.PROTECT,
        related_name="+"
    )
    last = models.ForeignKey(
        "JournalEntry",
        on_delete=models.PROTECT,
        related_name="+"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        get_latest_by = "created"

    @staticmethod
    def get_latest_report():
        """Return the lastest created report."""
        try:
            return Report.objects.earliest()
        except Report.DoesNotExist:
            return None

    @staticmethod
    def all_journal_entries_are_in_report():
        """
        Check if all journal entries already belong to a report.

        Return True if all journal entries belong to a report, False otherwise
        """
        return Report.get_latest_report().last == JournalEntry.objects.latest()

    @staticmethod
    def get_first_journal_entry_not_in_report():
        """
        Get the first journal entry that is not included in any report.

        If there are not reports, get the first journal entry created.
        """
        latest_report = Report.get_latest_report()
        if latest_report:
            previous_last = latest_report.last
            return Report.objects \
                .order_by("-created") \
                .exclude(created__lte=previous_last.created) \
                .first()
        else:
            return JournalEntry.objects.earliest()
