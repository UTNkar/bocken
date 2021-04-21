from django.test import TestCase
from django.utils.timezone import now, timedelta
from ..models import Agreement


class AgreementTestCase(TestCase):
    """Tests for the agreement model."""

    def test_has_expired(self):
        """Test if an agreement has expired."""
        agreement = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3039",
            email="mail@mail.se",
            expires=now().date() - timedelta(weeks=5)
        )

        self.assertTrue(agreement.has_expired())

    def test_has_not_expired(self):
        """Test if an agreement has not expired."""
        agreement = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3039",
            email="mail@mail.se",
            expires=now().date() + timedelta(weeks=5)
        )

        self.assertFalse(agreement.has_expired())
