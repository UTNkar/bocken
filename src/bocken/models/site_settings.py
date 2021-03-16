from .singleton import SingletonModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(SingletonModel):
    cost_per_mil = models.PositiveIntegerField(
        default=20,
        verbose_name=_("Cost per mil (kr)")
    )

    class Meta:
        verbose_name = _("Site settings")
        verbose_name_plural = _("Site settings")
