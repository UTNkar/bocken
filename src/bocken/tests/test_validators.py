from django.test import TestCase
from django.core.exceptions import ValidationError
from ..validators import validate_personnummer


class PersonnummerValidatorTests(TestCase):
    """Tests for the personnummer validator."""

    def test_normal_personnummer(self):
        """Test a normal personnummer."""
        try:
            validate_personnummer("980101-3039")
        except ValidationError:
            self.fail("A valid personnummer was considered invalid")

    def test_t_number(self):
        """Test a valid t-number."""
        try:
            validate_personnummer("19980101-T116")
        except ValidationError:
            self.fail("A valid t-number was considered invalid")

    def test_t_number_invalid_format(self):
        """Test a t-number that is in the incorrect format."""
        self.assertRaises(
            ValidationError, validate_personnummer, "980101-T116"
        )
