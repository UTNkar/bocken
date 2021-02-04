from phonenumbers import parse, is_valid_number
from django.core.exceptions import ValidationError
from personnummer import personnummer


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
        raise ValidationError("Invalid phonenumber")


def validate_personnummer(person_nummer):
    """
    Validate a personnummer.

    Raises ValidationError if the personnummer is not valid
    """
    valid = personnummer.valid(person_nummer)

    # If the personummer is invalid it could be a t-number.
    # Therefor we check if it is one of the letters allowed in a t-number
    # and replace it with a 1 since the letter is counted as one
    if not valid and (
        person_nummer[-4].upper() in [
            'T', 'R', 'S', 'U', 'W', 'X',
            'J', 'K', 'L', 'M', 'N'
        ]
    ):
        person_nummer = person_nummer[:-4] + '1' + person_nummer[-3:]
        valid = personnummer.valid(person_nummer)

        if not valid:
            raise ValidationError("Invalid personnummer")
