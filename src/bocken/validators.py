from phonenumbers import parse, is_valid_number, NumberParseException
from django.core.exceptions import ValidationError
from personnummer import personnummer
from django.utils.translation import gettext as _
from .utils import personnummer_is_t_number
from django.core.validators import RegexValidator

INVALID_PERSONNUMMER = _("Invalid personnummer")
INVALID_PHONENUMBER = _("Invalid phonenumber")


def validate_phonenumber(phonenumber):
    """
    Validate a phonenumber.

    Raises ValidationError if the phonenumber is not valid
    """
    try:
        parsed_phone = parse(phonenumber, "SE")
        if not is_valid_number(parsed_phone):
            raise ValidationError(INVALID_PHONENUMBER)

    except NumberParseException:
        raise ValidationError(INVALID_PHONENUMBER)


def validate_personnummer(person_nummer):
    """
    Validate a personnummer.

    Raises ValidationError if the personnummer is not valid
    """
    valid = personnummer.valid(person_nummer)

    # If the personummer is invalid it could be a t-number.
    if not valid:
        if not personnummer_is_t_number(person_nummer):
            raise ValidationError(INVALID_PERSONNUMMER)

        validate_tnummer(person_nummer)


def validate_tnummer(tnummer):
    """
    Validate a t number.

    Raises ValidationError if the personnummer is not valid
    """
    # T-numbers are a bit difficult to handle. Since the personnummer
    # library can't parse or format T-numbers, we must do it on our own.
    # The letter in a t-number is counted as a 1 when validating it.
    # Therefor we exchange the letter for a 1 and validate it as a normal
    # personnummer. It's not guaranteed that this will work in all cases.
    # We also need to make sure that the T-number is in the correct format
    # since the personnummer module can't format it

    RegexValidator(
        r'^[0-9]{8}[A-Za-z][0-9]{3}$',
        message=_('Your personnummer must be on the format YYYYMMDDXXXX')
    )(tnummer)

    tnummer = tnummer[:-4] + '1' + tnummer[-3:]
    valid = personnummer.valid(tnummer)

    if not valid:
        raise ValidationError(INVALID_PERSONNUMMER)
