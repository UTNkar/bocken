from django.db import models
from django.utils.translation import gettext_lazy as _
from . import JournalEntry
from collections import defaultdict
from django.template.defaultfilters import date
from django.utils.timezone import localtime
from django.utils import timezone


class Report(models.Model):
    """
    A report is a collection of journal entries.

    A report is created by adnministrators and shows how much each group has
    driven bocken between the first and last journal entry of a report
    """

    first = models.DateTimeField()

    last = models.DateTimeField()

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created")
    )

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        get_latest_by = "created"

    def __str__(self):
        return "{} - {}".format(
            date(localtime(self.first), "j F Y H:i"),
            date(localtime(self.last), "j F Y H:i")
        )

    def get_entries(self):
        """
        Get all journal entries within this report.

        Returns a queryset of journal entries
        """
        return JournalEntry.get_entries_between(self.first, self.last)

    def get_total_kilometers(self):
        """Get the total kilometers in this report."""
        entries = self.get_entries()

        total_kilometers = 0
        for entry in entries:
            total_kilometers += entry.get_total_distance()

        return total_kilometers

    def get_total_kilometers_for_groups(self):
        """
        Get the total kilometers driven for each group.

        If a group has not driven any kilometers they are not included.

        Returns a defaultdict with the group names as keys and their total
        kilometers driven as value.
        Ex. {'Baskå': 20}
        """
        entries = self.get_entries()

        total_kilometers = defaultdict(int)
        if entries:
            for entry in entries:
                total_kilometers[entry.get_group_display(
                )] += entry.get_total_distance()

        return total_kilometers

    @staticmethod
    def get_first_for_new_report():
        latest_report = Report.get_latest_report()
        if latest_report:
            first = latest_report.last
        else:
            try:
                first = JournalEntry.objects.earliest().created
            except JournalEntry.DoesNotExist:
                first = None

        return first

    @staticmethod
    def get_new_report():
        first = Report.get_first_for_new_report()
        last = timezone.now()

        entries = JournalEntry.get_entries_between(first, last)

        return first, last, entries

    @staticmethod
    def get_latest_report():
        """Return the lastest created report."""
        try:
            return Report.objects.latest()
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
            try:
                return JournalEntry.objects.exclude(
                    created__lte=previous_last.created
                ).earliest()
            except JournalEntry.DoesNotExist:
                # TODO: Make sure this is handled
                return None
        else:
            return JournalEntry.objects.earliest()
