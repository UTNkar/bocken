from phonenumbers import parse, is_valid_number
from django.core.exceptions import ValidationError
from personnummer import personnummer
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from .utils import personnummer_is_t_number


def validate_phonenumber(phonenumber):
    """
    Validate a phonenumber.

    Raises ValidationError if the phonenumber is not valid
    """
    try:
        parsed_phone = parse(phonenumber, "SE")
        if not is_valid_number(parsed_phone):
            raise Exception

        return phonenumber
    except Exception:
        raise ValidationError(_("Invalid phonenumber"))


def validate_personnummer(person_nummer):
    """
    Validate a personnummer.

    Raises ValidationError if the personnummer is not valid
    """
    valid = personnummer.valid(person_nummer)

    # If the personummer is invalid it could be a t-number.
    if not valid and personnummer_is_t_number(person_nummer):
        # T-numbers are a bit difficult to handle. Since the personnummer
        # library can't parse or format T-numbers, we must do it on our own.
        # This solution forces t-numbers to be the longest format. This way
        # we will always have the same format on all t-numbers which makes
        # lookup in the database easier.
        RegexValidator(
            r'^[0-9]{8}-.{4}$',
            message=_('Your personnummer must be on the format YYYYMMDD-XXXX')
        )(person_nummer)

        # The letter in a t-number is counted as a 1 when validating it.
        # Therefor we exchange the letter for a 1 and validate it as a normal
        # personnummer. It's not guaranteed that this will work in all cases
        person_nummer = person_nummer[:-4] + '1' + person_nummer[-3:]
        valid = personnummer.valid(person_nummer)

        if not valid:
            raise ValidationError(_("Invalid personnummer"))

    return person_nummer
