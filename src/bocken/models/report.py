from django.db import models


class Report(models.Model):
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
        return Report.objects.order_by("-created").first()
