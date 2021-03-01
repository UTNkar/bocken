from django.db import models
from bocken.validators import validate_phonenumber, validate_personnummer
from ..utils import format_personnummer
from ..fields import PhonenumberField
from django.utils.translation import gettext_lazy as _


class Agreement(models.Model):
    """
    Represents a person who has signed a bocken-agreement.

    When a person has signed a bocken-agreement they can drive bocken
    for 1 year. After that year they have to sign a new agreement.
    """

    number = models.IntegerField(
        primary_key=True,
        verbose_name=_("Agreement number")
    )
    name = models.CharField(
        max_length=120,
        verbose_name=_("Name")
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
        null=True
    )
    expires = models.DateField(
        verbose_name=_("Valid until")
    )

    class Meta:
        verbose_name = _("Agreement")
        verbose_name_plural = _("Agreements")

    def __str__(self): # noqa
        return "{} - {}".format(self.name, self.personnummer)

    def save(self, *args, **kwargs): # noqa
        self.personnummer = format_personnummer(self.personnummer)
        super(Agreement, self).save(*args, **kwargs)
