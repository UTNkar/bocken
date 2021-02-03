from django.db import models


class Report(models.Model):
    """
    A report is a collection of journal entries.

    A report is created by adnministrators and shows how much each group has
    driven bocken between the first and last journal entry of a report
    """

    first = models.ForeignKey(
        "JournalEntry",
        on_delete=models.PROTECT,
        related_name="+"
    )
    last = models.ForeignKey(
        "JournalEntry",
        on_delete=models.PROTECT,
        related_name="+"
    )
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_latest_report():
        """Return the lastest created report."""
        return Report.objects.order_by("-created").first()
