from .singleton import SingletonModel
from django.utils.translation import gettext_lazy as _


class SiteSettings(SingletonModel):

    class Meta:
        verbose_name = _("Site settings")
        verbose_name_plural = _("Site settings")
