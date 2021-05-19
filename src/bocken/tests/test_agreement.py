from django.test import TestCase
from django.utils.timezone import now, timedelta
from ..models import Agreement
from django.core import mail


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

    def test_automatic_reminder(self):
        """Test the automatic reminder for agreements."""
        agreement = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3039",
            email="mail@mail.se",
            expires=now().date() + timedelta(days=10)
        )

        agreement_without_email = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3040",
            expires=now().date() + timedelta(days=10)
        )

        Agreement.send_renewal_reminder_10_days_left()

        self.assertEqual(len(mail.outbox), 1)
        first_email = mail.outbox[0]

        self.assertTrue(agreement.email in first_email.recipients())
        self.assertTrue(
            agreement_without_email not in first_email.recipients()
        )
