from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from ..models import Agreement
from django.core import mail


class AgreementTestCase(TestCase):
    """Tests for the agreement model."""
    agreement1 = None

    def setUp(self):
        self.agreement1 = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3039",
            email="mail@mail.se",
            phonenumber="0733221122",
            expires=now().date() + timedelta(weeks=5)
        )

    def test_has_expired(self):
        """Test if an agreement has expired."""
        self.agreement1.expires = now().date() - timedelta(weeks=5)

        self.assertTrue(self.agreement1.has_expired())

    def test_has_not_expired(self):
        """Test if an agreement has not expired."""
        self.assertFalse(self.agreement1.has_expired())

    def test_automatic_reminder(self):
        """Test the automatic reminder for agreements."""
        self.agreement1.expires = now().date() + timedelta(days=10)
        self.agreement1.save()

        agreement_without_email = Agreement.objects.create(
            name="Name Nameson",
            personnummer="980101-5307",
            phonenumber="0733221144",
            expires=now().date() + timedelta(days=10)
        )

        Agreement.send_renewal_reminder_10_days_left()

        self.assertEqual(len(mail.outbox), 1)
        first_email = mail.outbox[0]

        self.assertTrue(self.agreement1.email in first_email.recipients())
        self.assertTrue(
            agreement_without_email not in first_email.recipients()
        )

    def test_personnummer_created_in_correct_format(self):
        # This assumes that the agreement was created with a different format
        # of the personnummer
        agreement = Agreement.objects.get(personnummer="199801013039")
        self.assertEqual(agreement.personnummer, "199801013039")

    def test_create_agreement_with_invalid_personnummer(self):
        invalid_personnummer = "980111-3366"
        self.assertRaises(
            ValidationError,
            Agreement.objects.create,
            name="Namn2 Namn2sson",
            personnummer=invalid_personnummer,
            email="mail2@mail2.se",
            phonenumber="0733221144"
        )
        self.assertRaises(
            Agreement.DoesNotExist,
            Agreement.objects.get,
            personnummer=invalid_personnummer
        )
