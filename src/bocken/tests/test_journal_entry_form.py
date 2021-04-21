from django.test import TestCase
from ..forms import JournalEntryForm
from ..models import JournalEntry, Agreement, JournalEntryGroup
from django.utils import timezone
from datetime import timedelta
from django.core import mail
from django.urls import reverse
from django.conf import settings


class JournalEntryFormTestCase(TestCase):
    """Tests for the journal entry form."""

    def setUp(self):  # noqa
        self.agreement = Agreement.objects.create(
            number=1,
            name="Name name",
            personnummer="980101-3039",
            phonenumber="0733221122",
            email="mail@mail.se",
            expires=timezone.now() + timedelta(days=365)
        )
        self.agreement.save()
        self.group = JournalEntryGroup.objects.create(
            name="Gruppen",
            main_group='lg_and_board',
        )

    def test_initial_meter_start(self):
        """
        Test the initial meter start.

        It should be set to the meter stop of the latest entry.
        """
        JournalEntry.objects.create(
            agreement=self.agreement,
            group=self.group,
            meter_start=40,
            meter_stop=49
        )

        form = JournalEntryForm()
        self.assertEqual(form.initial['meter_start'], 49)

    def test_invalid_personnummer(self):
        """Test form submission with invalid personnummer."""
        form_data = {
            'personnummer': '980101-1111',
            'group': self.group.id,
            'meter_start': 40,
            'meter_stop': 58,
            'confirm': True
        }
        form = JournalEntryForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('personnummer' in form.errors)

    def test_too_small_meter_start(self):
        """Test when meter start is smaller than the latest entry."""
        JournalEntry.objects.create(
            agreement=self.agreement,
            group=self.group,
            meter_start=40,
            meter_stop=49
        )
        form_data = {
            'personnummer': '980101-1111',
            'group': self.group.id,
            'meter_start': 45,
            'meter_stop': 58,
            'confirm': True
        }

        form = JournalEntryForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('meter_start' in form.errors)

    def test_too_small_meter_stop(self):
        """Test when meter stop is smaller than meter start."""
        form_data = {
            'personnummer': '980101-1111',
            'group': self.group.id,
            'meter_start': 45,
            'meter_stop': 39,
            'confirm': True
        }

        form = JournalEntryForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('meter_stop' in form.errors)

    def test_valid_submission(self):
        """Test a valid submission."""
        form_data = {
            'personnummer': '980101-3039',
            'group': self.group.id,
            'meter_start': 45,
            'meter_stop': 49,
            'confirm': True,
            'g-recaptcha-response': 'PASSED'
        }
        form = JournalEntryForm(form_data)
        self.assertTrue(form.is_valid())
        form.save()

        latest_entry = JournalEntry.get_latest_entry()
        self.assertEqual(latest_entry.agreement, self.agreement)
        self.assertEqual(latest_entry.meter_start, 45)

    def test_different_personnummer_format(self):
        """
        Test a personnummer that has a different format.

        The personnummer has a different format than the one that was used
        when creating the agreement. The personnummer should still be able to
        get the correct agreement.
        """
        form_data = {
            'personnummer': '19980101-3039',
            'group': self.group.id,
            'meter_start': 45,
            'meter_stop': 49,
            'confirm': True,
            'g-recaptcha-response': 'PASSED'
        }
        form = JournalEntryForm(form_data)
        self.assertTrue(form.is_valid())
        form.save()

        latest_entry = JournalEntry.get_latest_entry()
        self.assertEqual(latest_entry.agreement, self.agreement)

    def test_expired_agreement(self):
        """
        Test when a form is submitted with an expired agreement.

        A message should be set and an email should be sent to the
        klubbmästare.
        """
        self.agreement.expires = timezone.now().date() - timedelta(days=365)
        self.agreement.save()

        form_data = {
            'personnummer': '19980101-3039',
            'group': self.group.id,
            'meter_start': 45,
            'meter_stop': 49,
            'confirm': True,
            'g-recaptcha-response': 'PASSED'
        }
        response = self.client.post(
            reverse('add-entry'), form_data, follow=True
        )
        self.assertRedirects(response, reverse('add-entry-success'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        self.assertEqual(len(mail.outbox), 1)
        first_email = mail.outbox[0]

        # Test that name and personnummer actually is in the email
        self.assertTrue(self.agreement.name in first_email.body)
        self.assertTrue(self.agreement.personnummer in first_email.body)

        self.assertTrue(
            settings.KLUBBMASTARE_EMAIL in first_email.recipients()
        )
