from django.db import models
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
# Report must be imported like this to avoid circular import
import bocken.models.report as report


class JournalEntry(models.Model):
    """
    An entry that drivers adds to the journal.

    When a person with an agreement has driven bocken they create an entry
    that describes how far they have driven
    """

    agreement = models.ForeignKey(
        "Agreement",
        on_delete=models.PROTECT,
        verbose_name=_("Agreement")
    )
    group = models.ForeignKey(
        "JournalEntryGroup",
        on_delete=models.PROTECT,
        verbose_name=_("Group")
    )
    meter_start = models.PositiveIntegerField(
        verbose_name=_("Meter at start")
    )
    meter_stop = models.PositiveIntegerField(
        verbose_name=_("Meter at stop")
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")
        get_latest_by = "meter_stop"

    def __str__(self):  # noqa
        return "{} - {}".format(
            self.created_formatted,
            self.agreement.name
        )

    @property
    def created_formatted(self):
        """Return the created date in the correct format."""
        return date_format(self.created, format='j F Y H:i')

    def get_total_distance(self):
        """Calculate the total distance driven."""
        return self.meter_stop - self.meter_start
    get_total_distance.short_description = _("Driven Distance (km)")

    def meter_start_gap_marker(self):
        try:
            previous_entry = JournalEntry.objects.filter(
                meter_stop__lt=self.meter_stop
            ).latest()
        except JournalEntry.DoesNotExist:
            return self.meter_start

        if previous_entry.meter_stop != self.meter_start:
            return format_html(
                (
                    '<p '
                    'style="background: rgb(220, 38, 38);'
                    'color: white; margin:0; padding:0;'
                    '">{}</p>'
                ),
                self.meter_start
            )
        else:
            return self.meter_start
    meter_start_gap_marker.admin_order_field = 'meter_start'
    meter_start_gap_marker.short_description = meter_start.verbose_name

    def meter_stop_gap_marker(self):
        try:
            previous_entry = JournalEntry.objects.filter(
                meter_stop__gt=self.meter_stop
            ).earliest()
        except JournalEntry.DoesNotExist:
            return self.meter_stop

        if previous_entry.meter_start != self.meter_stop:
            return format_html(
                (
                    '<p '
                    'style="background: rgb(220, 38, 38);'
                    'color: white; margin:0; padding:0;'
                    '">{}</p>'
                ),
                self.meter_stop
            )
        else:
            return self.meter_stop
    meter_stop_gap_marker.admin_order_field = 'meter_stop'
    meter_stop_gap_marker.short_description = meter_stop.verbose_name

    @staticmethod
    def entries_exists():
        """
        Check if there exists any journal entries.

        Returns True if there are not journal entries in the database,
        False otherwise
        """
        return JournalEntry.objects.exists()

    @staticmethod
    def get_latest_entry():
        """Get the entry that was last created."""
        try:
            return JournalEntry.objects.latest()
        except JournalEntry.DoesNotExist:
            return None

    @staticmethod
    def get_entries_between(start, end):
        """
        Get all entries between the timestamps start and end.

        Returns all journal entries within the time range. All journal entries
        that are equal to start or end are included.
        """
        entries = JournalEntry.objects.filter(
            created__range=(start, end)
        )
        return entries

    @staticmethod
    def get_entries_since_last_report_amount():
        """Get the number of new entries since the last report."""
        latest_report = report.Report.get_latest_report()
        if latest_report:
            entries = JournalEntry.objects.exclude(
                created__lte=latest_report.created
            )
            return entries.count()
        else:
            return JournalEntry.objects.count()

    @staticmethod
    def get_three_latest_entries():
        """Get the three latest entries."""
        return JournalEntry.objects.order_by("-created")[:3]
