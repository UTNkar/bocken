from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from ..models import Agreement
from django.core import mail


class AgreementTestCase(TestCase):
    """Tests for the agreement model."""

    agreement1 = None

    def setUp(self):  # noqa
        self.agreement1 = Agreement.objects.create(
            name="Name Nameson",
            personnummer="19980101-3039",
            email="mail@mail.se",
            phonenumber="0733221122",
        )

    def test_has_expired(self):
        """Test if an agreement has expired."""
        self.agreement1.expires = now().date() - timedelta(days=1)

        self.assertTrue(self.agreement1.has_expired())

    def test_has_not_expired_today(self):
        """Test if an agreement has not expired today."""
        self.agreement1.expires = now().date()

        self.assertFalse(self.agreement1.has_expired())

    def test_has_not_expired(self):
        """Test if an agreement has not expired."""
        self.agreement1.expires = now().date() + timedelta(days=1)
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

    def test_personnummer_saved_in_correct_format(self):
        """Test that personnummer is saved in the correct format."""
        self.agreement1.personnummer = '19980101-3039'
        self.agreement1.save()

        agreement = Agreement.objects.get(personnummer="199801013039")
        self.assertEqual(agreement.personnummer, "199801013039")

    def test_create_agreement_with_invalid_personnummer(self):
        """Test that an agreement can not be created with an invalid personnummer."""  # noqa: E501
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

    def test_t_number_wrong_format(self):
        """Test that an agreement can not be created with the wrong format on the T number."""  # noqa: E501
        self.assertRaises(
            ValidationError,
            Agreement.objects.create,
            name="Tname sonson",
            personnummer="19980101-T728",
            email="mailtt@maitttl.se",
            phonenumber="0733225566"
        )

    def test_t_number_correct_format(self):
        """Test that an agreement with correct format on the T number can be created."""  # noqa: E501
        try:
            Agreement.objects.create(
                name="Tname sonson",
                personnummer="19980101T728",
                email="mailtt@maitttl.se",
                phonenumber="0733225566"
            )
        except ValidationError:
            self.fail(
                "An agreement with a valid T number could not be created"
            )
