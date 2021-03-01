from phonenumbers import parse, format_number, PhoneNumberFormat
from django.db import models


class PhonenumberField(models.CharField):
    """A custom field for phonenumbers."""

    def from_db_value(self, value, expression, connection):
        """Format the phonenumber when it is fetched from the database."""
        try:
            parsed_number = parse(value, "SE")
            number_format = \
                PhoneNumberFormat.NATIONAL \
                if parsed_number.country_code == 46 \
                else PhoneNumberFormat.INTERNATIONAL

            return format_number(
                parsed_number,
                number_format
            )
        except Exception:
            return value
