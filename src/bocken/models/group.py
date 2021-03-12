from django.db import models


class JournalEntryGroup(models.Model):
    name = models.CharField(max_length=60)
    cost_per_mil = models.PositiveIntegerField(default=20)
    starting_fee = models.PositiveIntegerField(default=0)
