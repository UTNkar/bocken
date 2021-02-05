from django.db import models


class JournalEntry(models.Model):
    """
    An entry that drivers adds to the journal.

    When a person with an agreement has driven bocken they create an entry
    that describes how far they have driven
    """

    agreement = models.ForeignKey("Agreement", on_delete=models.PROTECT)
    group = models.CharField(max_length=120, choices=[('td', 'TD')])
    meter_start = models.IntegerField()
    meter_stop = models.IntegerField()
    total_distance = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def calculate_total_distance(self):
        """Calculate the total distance driven."""
        return self.meter_stop - self.meter_start

    def get_latest_entry():
        try:
            return JournalEntry.objects.latest('-created')
        except JournalEntry.DoesNotExist:
            return None
