from django.db import models
from django.utils.translation import gettext_lazy as _


class JournalEntryGroup(models.Model):
    """Represents a group that can be selected in a journal entry."""

    name = models.CharField(
        max_length=60,
        verbose_name=_("Name")
    )
    main_group = models.CharField(
        max_length=30,
        choices=(
            (
                'committees_workgroups',
                _("UTN's committees and workgroups")
            ),
            ('lg_and_board', _("UTN's management team and board")),
            ('fum', _("FUM")),
            ('other_officials', _("Other officials within UTN")),
            ('sections', _("Sections")),
            ('cooperations', _("Cooperations")),
        ),
        verbose_name=_("Main group")
    )

    class Meta:
        verbose_name = _("Journal entry group")
        verbose_name_plural = _("Journal entry groups")

    def __str__(self):  # noqa
        return self.name
