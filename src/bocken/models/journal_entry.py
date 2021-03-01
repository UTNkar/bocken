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
    total_distance = models.PositiveIntegerField(
        verbose_name=_("Driven Distance (km)")
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")

    def __str__(self): # noqa
        return "{} - {}".format(
            date_format(self.created, format='j F Y H:i'),
            self.agreement.name
        )

    def calculate_total_distance(self):
        """Calculate the total distance driven."""
        return self.meter_stop - self.meter_start

    @staticmethod
    def get_latest_entry():
        """Get the entry that was last created."""
        try:
            return JournalEntry.objects.latest('created')
        except JournalEntry.DoesNotExist:
            return None

    def save(self, *args, **kwargs): # noqa
        self.total_distance = self.calculate_total_distance()
        super(JournalEntry, self).save(*args, **kwargs)
