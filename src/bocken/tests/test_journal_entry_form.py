from datetime import timedelta

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..forms import JournalEntryForm
from ..models import Agreement, JournalEntry, JournalEntryGroup, Vehicle


class JournalEntryFormTestCase(TestCase):
    """Tests for the journal entry form."""

    def setUp(self):  # noqa
        self.agreement = Agreement.objects.create(
            name="Name name",
            personnummer="980101-3039",
            phonenumber="0733221122",
            car_agreement=True,
            email="mail@mail.se",
            expires=timezone.now() + timedelta(days=365),
        )
        self.t_number_agreement = Agreement.objects.create(
            name="Blipp blopp",
            personnummer="19980101T728",
            phonenumber="0733221144",
            car_agreement=True,
            bike_agreement=False,
            email="mail2@mail2.se",
        )
        self.bike_agreement = Agreement.objects.create(
            name="Blipp blopp",
            personnummer="189001069815",
            phonenumber="0733221144",
            car_agreement=False,
            bike_agreement=True,
            email="mail2@mail2.se",
        )
        self.car_agreement = Agreement.objects.create(
            name="Blipp blopp",
            personnummer="189001019802",
            phonenumber="0733221144",
            car_agreement=False,
            bike_agreement=True,
            email="mail2@mail2.se",
        )
        self.group = JournalEntryGroup.objects.create(
            name="Gruppen",
            main_group="lg_and_board",
        )
        self.vehicle = Vehicle.objects.create(vehicle_name="TockenKrocken", car=True)
        self.form_data = {
            "personnummer": "980101-3039",
            "group": self.group.id,
            "vehicle": self.vehicle.id,  # This id correlates to bocken as should be the default for all current journal entries
            "meter_start": 45,
            "meter_stop": 49,
            "confirm": True,
            "g-recaptcha-response": "PASSED",
        }

    def test_initial_meter_start(self):
        """
        Test the initial meter start.

        It should be set to the meter stop of the latest entry.
        """
        JournalEntry.objects.create(
            agreement=self.agreement,
            vehicle=self.vehicle,
            group=self.group,
            meter_start=40,
            meter_stop=49,
        )

        form = JournalEntryForm()
        self.assertEqual(form.initial["meter_start"], 49)

    def test_invalid_personnummer(self):
        """Test form submission with invalid personnummer."""
        self.form_data["personnummer"] = "980101-1111"

        form = JournalEntryForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("personnummer" in form.errors)

    def test_too_small_meter_start(self):
        """Test when meter start is smaller than the latest entry."""
        JournalEntry.objects.create(
            agreement=self.agreement,
            vehicle=self.vehicle,
            group=self.group,
            meter_start=40,
            meter_stop=49,
        )

        self.form_data["meter_start"] = 45

        form = JournalEntryForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("meter_start" in form.errors)

    def test_too_small_meter_stop(self):
        """Test when meter stop is smaller than meter start."""
        self.form_data["meter_stop"] = 25

        form = JournalEntryForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("meter_stop" in form.errors)

    def test_valid_submission(self):
        """Test a valid submission."""
        form = JournalEntryForm(self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        latest_entry = JournalEntry.get_latest_entry()
        self.assertEqual(latest_entry.agreement, self.agreement)
        self.assertEqual(latest_entry.meter_start, 45)
        self.assertEqual(latest_entry.meter_stop, 49)

    def test_different_personnummer_format(self):
        """
        Test a personnummer that has a different format.

        The personnummer has a different format than the one that was used
        when creating the agreement. The personnummer should still be able to
        get the correct agreement.
        """
        form_data = {
            "personnummer": "19980101-3039",
            "group": self.group.id,
            "vehicle": self.vehicle.id,
            "meter_start": 45,
            "meter_stop": 49,
            "confirm": True,
            "g-recaptcha-response": "PASSED",
        }
        form = JournalEntryForm(form_data)
        self.assertTrue(form.is_valid())
        form.save()

        latest_entry = JournalEntry.get_latest_entry()
        self.assertEqual(latest_entry.agreement, self.agreement)

    def test_incorrect_vehicle_has_agreement_for_bikes(self):
        """
        Test that a user which may only drive cars cannot submit a entry for bikes.

        A error should be added to to the form and it should be the only error available
        in the form.
        """
        vehicle = Vehicle.objects.exclude(id=self.vehicle.id).filter(car=False).get()
        form_data = {
            "personnummer": "19980101-3039",
            "group": self.group.id,
            "vehicle": vehicle.id,
            "meter_start": 45,
            "meter_stop": 49,
            "confirm": True,
            "g-recaptcha-response": "PASSED",
        }
        form = JournalEntryForm(form_data)
        self.assertFalse(form.is_valid())
        all_errors = [(x, form.has_error(x)) for x in form.fields if form.has_error(x)]
        self.assertTrue(len(all_errors) == 1)
        self.assertTrue(all_errors[0][0] == "vehicle")

    def test_correct_vehicle_has_agreement_for_cars(self):
        """
        Test that a user may drive vehicles of the same type, i.e. cars.
        """
        vehicle = (
            Vehicle.objects.exclude(id=self.vehicle.id).filter(car=True).get()
        )  # this picks a car which is not the initial vehicle type created within this test suite
        form_data = {
            "personnummer": "19980101-3039",
            "group": self.group.id,
            "vehicle": vehicle.id,
            "meter_start": 45,
            "meter_stop": 49,
            "confirm": True,
            "g-recaptcha-response": "PASSED",
        }
        form = JournalEntryForm(form_data)
        self.assertTrue(form.is_valid())
        all_errors = [(x, form.has_error(x)) for x in form.fields if form.has_error(x)]
        self.assertTrue(len(all_errors) == 0)

    def test_expired_agreement(self):
        """
        Test when a form is submitted with an expired agreement.

        A message should be set and an email should be sent to the
        klubbmästare.
        """
        self.agreement.expires = timezone.now().date() - timedelta(days=365)
        self.agreement.save()

        response = self.client.post(reverse("add-entry"), self.form_data, follow=True)
        self.assertRedirects(response, reverse("add-entry-success"))

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)

        self.assertEqual(len(mail.outbox), 1)
        first_email = mail.outbox[0]

        # Test that name and personnummer actually is in the email
        self.assertTrue(self.agreement.name in first_email.body)
        self.assertTrue(self.agreement.personnummer in first_email.body)

        self.assertTrue(settings.KLUBBMASTARE_EMAIL in first_email.recipients())

    def test_gap_notification(self):
        """Test that an email is sent if a gap occurs."""
        # Create an earlier journal entry
        JournalEntry.objects.create(
            agreement=self.agreement,
            vehicle=self.vehicle,
            group=self.group,
            meter_start=45,
            meter_stop=49,
        )

        self.form_data["meter_start"] = 60
        self.form_data["meter_stop"] = 70
        self.form_data["vehicle"] = self.vehicle.id
        response = self.client.post(reverse("add-entry"), self.form_data, follow=True)
        self.assertRedirects(response, reverse("add-entry-success"))

        self.assertEqual(len(mail.outbox), 1)
        first_email = mail.outbox[0]

        # Test that the name actually is in the email
        self.assertTrue(self.agreement.name in first_email.body)

        self.assertTrue(settings.KLUBBMASTARE_EMAIL in first_email.recipients())

    def test_no_gap_notification_different_vehicles(self):
        """Test that an email is not sent if a gap occurs for different vehicles."""
        # Create an earlier journal entry
        JournalEntry.objects.create(
            agreement=self.agreement,
            vehicle=self.vehicle,
            group=self.group,
            meter_start=45,
            meter_stop=49,
        )
        vehicle = Vehicle.objects.exclude(id=self.vehicle.id).filter(car=True).get()
        self.form_data["meter_start"] = 60
        self.form_data["meter_stop"] = 70
        self.form_data["vehicle"] = vehicle.id  # comparing bocken with trockenkrocken

        response = self.client.post(reverse("add-entry"), self.form_data, follow=True)
        self.assertEqual(len(mail.outbox), 0)

    def test_t_number_wrong_format(self):
        """Test a submission with the wrong format on the T number."""
        self.form_data["personnummer"] = "19980101-T728"

        form = JournalEntryForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("personnummer" in form.errors)
        self.assertIn("YYYYMMDDXXXX", form.errors["personnummer"][0])

    def test_t_number(self):
        """Test submitting with the correct format on T-number."""
        self.form_data["personnummer"] = "19980101T728"

        form = JournalEntryForm(self.form_data)
        self.assertTrue(form.is_valid())
