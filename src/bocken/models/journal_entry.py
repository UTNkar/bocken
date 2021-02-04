from django.db import models


class JournalEntry(models.Model):
    """
    An entry that drivers adds to the journal.

    When a person with an agreement has driven bocken they create an entry
    that describes how far they have driven
    """

    agreement_number = models.ForeignKey("Agreement", on_delete=models.PROTECT)
    name = models.TextField(max_length=120)
    group = models.TextField(choices=())
    meter_start = models.IntegerField()
    meter_stop = models.IntegerField()
    total_distance = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def calculate_total_distance(self):
        """Calculate the total distance driven."""
        return self.meter_stop - self.meter_start
