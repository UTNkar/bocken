from django.db import models
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    """Represents a vehicle that can be selected in a journal entry."""

    vehicle_type = models.CharField(
        max_length=60,
        verbose_name=_("Type")
    )
    vehicle_meter_start = models.PositiveIntegerField(
        verbose_name=_("Meter at start (Latest Entry)"),
        default=0
    )
    vehicle_meter_stop = models.PositiveIntegerField(
        verbose_name=_("Meter at stop (Latest Entry)"),
        default=0
    )

    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self):  # noqa
        return self.vehicle_type
