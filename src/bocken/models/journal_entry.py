from django.db import models
from ..constants import (
    JOURNAL_ENTRY_COMMITTEES_WORKGROUPS,
    JOURNAL_ENTRY_COOPERATINS,
    JOURNAL_ENTRY_FUM,
    JOURNAL_ENTRY_LG_AND_BOARD,
    JOURNAL_ENTRY_OTHER_OFFICIALS,
    JOURNAL_ENTRY_SECTIONS,
)
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _


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
    group = models.CharField(
        max_length=120,
        choices=(
            JOURNAL_ENTRY_COMMITTEES_WORKGROUPS +
            JOURNAL_ENTRY_COOPERATINS +
            JOURNAL_ENTRY_FUM +
            JOURNAL_ENTRY_LG_AND_BOARD +
            JOURNAL_ENTRY_OTHER_OFFICIALS +
            JOURNAL_ENTRY_SECTIONS
        ),
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
        get_latest_by = "created"

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

    @staticmethod
    def get_latest_entry():
        """Get the entry that was last created."""
        try:
            return JournalEntry.objects.latest()
        except JournalEntry.DoesNotExist:
            return None

    @staticmethod
    def get_entries_between(first, last):
        entries = JournalEntry.objects.filter(
            created__range=(first, last)
        )
        return entries
