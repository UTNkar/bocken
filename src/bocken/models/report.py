from django.db import models
from django.utils.translation import gettext_lazy as _
from . import JournalEntryGroup
from django.template.defaultfilters import date
from django.utils.timezone import localtime
from django.utils import timezone
from django.db.models import Sum
from ..utils import kilometers_to_mil
from django.conf import settings
# Journal entry must be imported like this to avoid circular import
import bocken.models.journal_entry as journal_entry
from dateutil.relativedelta import relativedelta


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

    cost_per_mil = models.PositiveIntegerField(
        default=settings.COST_PER_MIL_DEFAULT,
        verbose_name=_("Cost per mil (kr)"),
        help_text=_(
            "Each report can have a different cost per mil. This allows "
            "the cost per mil to be changed without affecting previous reports"
        )
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
        return journal_entry.JournalEntry.get_entries_between(
            self.first, self.last
        )

    def get_total_kilometers_driven(self):
        """Return the total kilometers that have been driven in this report."""
        entries = self.get_entries()
        first = entries.earliest()
        last = entries.latest()

        return last.meter_stop - first.meter_start

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
        # What it does is that it calculates the total distance driven for each
        # journal entry and then sums them up for each group, giving us the
        # total kilometers for each group.
        kilometers_for_groups = entries.values("group").annotate(
            total_kilometers=Sum("meter_stop") - Sum("meter_start")
        ).order_by("group__name")

        statistics = []
        for group in kilometers_for_groups:
            kilometers = group['total_kilometers']
            actual_group = JournalEntryGroup.objects.get(
                pk=group['group']
            )
            mil = kilometers_to_mil(kilometers)
            cost = self.calculate_cost_for_mil(mil)

            statistics.append({
                'group': actual_group,
                'kilometers': kilometers,
                'mil': mil,
                'cost': cost
            })

        return statistics

    def get_total_statistics(self):
        """
        Get the total values from the statisitcs in this report.

        Returns a dict with the following structure:
        {
            'total_kilometers': Total kilometers driven in this report,
            'total_mil': Total mil driven in this report,
            'total_cost': Total cost for all groups in the report
        }
        """
        statistics_for_groups = self.get_statistics_for_groups()

        total_kilometers = sum(
            statistic['kilometers'] for statistic in statistics_for_groups
        )
        total_mil = sum(
            statistic['mil'] for statistic in statistics_for_groups
        )
        total_cost = sum(
            statistic['cost'] for statistic in statistics_for_groups
        )

        return {
            'total_kilometers': total_kilometers,
            'total_mil': total_mil,
            'total_cost': total_cost
        }

    def calculate_cost_for_mil(self, mil: int):
        """
        Calculate the total cost for driving a certain amount of mil.

        Parameters:
        mil (int): The total mil driven

        Returns the cost in kr
        """
        return mil * self.cost_per_mil

    def calculate_lost_cost(self):
        """
        Calculate the lost cost for the report.

        Returns a dict: {
            lost_kilometers: the total number of kilometers lost,
            lost_cost: the total cost lost
        }
        """
        total_driven = self.get_total_kilometers_driven()
        total_logged = self.get_total_statistics()['total_kilometers']

        lost_kilometers = total_driven - total_logged
        lost_mil = kilometers_to_mil(lost_kilometers)
        lost_cost = self.calculate_cost_for_mil(lost_mil)

        return {
            'lost_kilometers': lost_kilometers,
            'lost_cost': lost_cost
        }

    @staticmethod
    def get_first_for_new_report():
        """
        Get the first journal entry when creating a new report.

        The first entry in a new report is the last entry in the previous
        report. If there are no previous reports, the first entry is the
        first ever created journal entry. If there are no journal entries,
        a report can not be created.

        Returns the journal entry that should be used as the first in a new
        report.
        """
        latest_report = Report.get_latest_report()
        if latest_report:
            first = latest_report.last
        else:
            try:
                first = journal_entry.JournalEntry.objects.earliest().created
            except journal_entry.JournalEntry.DoesNotExist:
                first = None

        return first

    @staticmethod
    def get_new_report_details():
        """
        Get all details for a new report.

        Returns a tuple of the first and last journal entry for the new report
        and all journal entries between the first and last.
        """
        first = Report.get_first_for_new_report()
        last = timezone.now()

        entries = journal_entry.JournalEntry.get_entries_between(first, last)

        return first, last, entries

    @staticmethod
    def get_latest_report():
        """Return the lastest created report."""
        try:
            return Report.objects.latest()
        except Report.DoesNotExist:
            return None

    @staticmethod
    def delete_older_than_one_year():
        """
        Delete all reports that are older than one year.

        Also deletes all journal entries in those reports.
        """
        one_year_ago = timezone.now() - relativedelta(years=1)
        reports_to_delete = Report.objects.filter(
            created__date__lte=one_year_ago
        )

        # Delete all related journal entries
        for report in reports_to_delete:
            report.get_entries().delete()

        reports_to_delete.delete()
