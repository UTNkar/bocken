from django.db import models
from bocken.validators import validate_phonenumber, validate_personnummer
from ..utils import format_personnummer
from ..fields import PhonenumberField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta
from django.utils.html import format_html
from django.template.defaultfilters import date


def get_default_expires():
    """Return the default expires date for an agreement."""
    return now().date() + timedelta(days=365)


class Agreement(models.Model):
    """
    Represents a person who has signed a bocken-agreement.

    When a person has signed a bocken-agreement they can drive bocken
    for 1 year. After that year they have to sign a new agreement.
    """

    name = models.CharField(
        max_length=120,
        verbose_name=_("Name"),
        help_text=_("First and last name")
    )

    personnummer = models.CharField(
        max_length=13,
        validators=[validate_personnummer],
        unique=True
    )

    phonenumber = PhonenumberField(
        max_length=20,
        validators=[validate_phonenumber],
        verbose_name=_("Phonenumber")
    )

    # Email is allowed to be null since we don't have an email address to
    # everyone who has an agreement at the time of creation of this system.
    # TODO: Remove blank and null when there is an email address for all
    # agreements
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "The person's private email. Should not be an email ending in "
            "@utn.se."
        ),
    )

    expires = models.DateField(
        verbose_name=_("Valid until"),
        default=get_default_expires,
        help_text=_("Agreements are valid for 1 year by default.")
    )

    class Meta:
        verbose_name = _("Agreement")
        verbose_name_plural = _("Agreements")
        ordering = ('name',)
        indexes = [
            models.Index(
                fields=['name', 'personnummer']
            )
        ]

    def __str__(self):  # noqa
        return "{} - {}".format(self.name, self.personnummer)

    def has_expired(self):
        """Check if an agreement has expired."""
        return self.expires <= now().date()

    def expires_colored(self):
        """
        Color the expires field red if the agreement has expired.

        This is used in the admin pages.
        """
        if self.has_expired():
            return format_html(
                (
                    '<p '
                    'style="background: rgb(220, 38, 38);'
                    'color: white; margin:0; padding:0;'
                    '">{}</p>'
                ),
                date(self.expires),  # Format the date correctly
            )
        else:
            return self.expires
    expires_colored.admin_order_field = 'expires'

    def save(self, *args, **kwargs):  # noqa
        self.personnummer = format_personnummer(self.personnummer)
        super(Agreement, self).save(*args, **kwargs)
