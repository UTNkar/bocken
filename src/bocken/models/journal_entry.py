from django.db import models
from ..constants import (
    JOURNAL_ENTRY_COMMITTEES_WORKGROUPS,
    JOURNAL_ENTRY_COOPERATINS,
    JOURNAL_ENTRY_FUM,
    JOURNAL_ENTRY_LG_AND_BOARD,
    JOURNAL_ENTRY_OTHER_OFFICIALS,
    JOURNAL_ENTRY_SECTIONS,
)


class JournalEntry(models.Model):
    """
    An entry that drivers adds to the journal.

    When a person with an agreement has driven bocken they create an entry
    that describes how far they have driven
    """

    agreement = models.ForeignKey("Agreement", on_delete=models.PROTECT)
    group = models.CharField(
        max_length=120,
        choices=(
            JOURNAL_ENTRY_COMMITTEES_WORKGROUPS +
            JOURNAL_ENTRY_COOPERATINS +
            JOURNAL_ENTRY_FUM +
            JOURNAL_ENTRY_LG_AND_BOARD +
            JOURNAL_ENTRY_OTHER_OFFICIALS +
            JOURNAL_ENTRY_SECTIONS
        )
    )
    meter_start = models.PositiveIntegerField()
    meter_stop = models.PositiveIntegerField()
    total_distance = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

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
