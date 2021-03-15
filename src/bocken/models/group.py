from django.db import models
from django.utils.translation import gettext_lazy as _


class JournalEntryGroup(models.Model):
    name = models.CharField(max_length=60)
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
    cost_per_mil = models.PositiveIntegerField(default=20)
    starting_fee = models.PositiveIntegerField(default=0)

    def __str__(self):  # noqa
        return self.name

    def calculate_total_cost(self, mil):
        return mil * self.cost_per_mil + self.starting_fee
