from django.db import models
from bocken.validators import validate_phonenumber, validate_personnummer
from ..utils import format_personnummer


class Agreement(models.Model):
    """
    Represents a person who has signed a bocken-agreement.

    When a person has signed a bocken-agreement they can drive bocken
    for 1 year. After that year they have to sign a new agreement.
    """

    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    personnummer = models.CharField(
        max_length=13,
        validators=[validate_personnummer],
        unique=True
    )
    phonenumber = models.CharField(
        max_length=20,
        validators=[validate_phonenumber]
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
    expires = models.DateField()

    def save(self, *args, **kwargs): # noqa
        self.personnummer = format_personnummer(self.personnummer)
        super(Agreement, self).save(*args, **kwargs)
