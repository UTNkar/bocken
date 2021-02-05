from django.db import models
from bocken.validators import validate_phonenumber, validate_personnummer


class Agreement(models.Model):
    """
    Represents a person who has signed a bocken-agreement.

    When a person has signed a bocken-agreement they can drive bocken
    for 1 year. After that year they have to sign a new agreement.
    """

    number = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=120)
    personnummer = models.TextField(
        max_length=13,
        validators=[validate_personnummer],
        unique=True
    )
    phonenumber = models.TextField(
        max_length=20,
        validators=[validate_phonenumber]
    )
    email = models.EmailField(unique=True)
    signed = models.DateField(auto_now_add=True)
