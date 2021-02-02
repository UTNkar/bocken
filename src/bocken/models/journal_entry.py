from django.db import models


class JournalEntry(models.Model):
    agreement_number = models.ForeignKey("Agreement", on_delete=models.PROTECT)
    name = models.TextField(max_length=120)
    group = models.TextField(choices=())
    meter_start = models.IntegerField()
    meter_stop = models.IntegerField()
    total_distance = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def calculate_total_distance(self):
        return self.meter_stop - self.meter_start
