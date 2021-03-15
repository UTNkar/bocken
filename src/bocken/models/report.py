from django.db import models
from django.utils.translation import gettext_lazy as _
from . import JournalEntry, JournalEntryGroup
from django.template.defaultfilters import date
from django.utils.timezone import localtime
from django.utils import timezone
from django.db.models import Sum
from ..utils import kilometers_to_mil


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

    def __str__(self):  # noqa
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

    def get_statistics_for_groups(self):
        """
        Get statistics for each group that is a part of this report.

        Included in these statistics are
        - The group
        - Total kilometers driven
        - Total mil driven
        - Total cost each group has to pay

        Returns list of dicts where each dict has the following structure
        {
            'group': JournalEntryGroup instance
            'kilometers': Total kilometers (int),
            'mil': Total mil (int),
            'cost': Total cost (int)
        }
        """
        entries = self.get_entries()

        # Calulate the total kilometers for each group by performing a
        # "group by" query in the database. It can be a bit difficult
        # to understand but the documentation has an explanation for it.
        # https://docs.djangoproject.com/en/3.1/topics/db/aggregation/#values
        kilometers_for_groups = entries.values("group").annotate(
            total_kilometers=Sum("meter_stop") - Sum("meter_start")
        ).order_by("group__name")

        statistics = []
        for group in kilometers_for_groups:
            kilometers = group['total_kilometers']
            actual_group = JournalEntryGroup.objects.get(pk=group['group'])
            mil = kilometers_to_mil(kilometers)
            cost = actual_group.calculate_total_cost(mil)

            statistics.append({
                'group': actual_group,
                'kilometers': kilometers,
                'mil': mil,
                'cost': cost
            })

        return statistics

    def get_total_kilometers(self):
        """Get the total kilometers in this report."""
        entries = self.get_entries()

        return entries.aggregate(
            total=Sum("meter_stop") - Sum("meter_start")
        )['total']

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
