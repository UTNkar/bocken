from django.test import TestCase
from ..models import JournalEntry, Agreement, JournalEntryGroup, Report
from django.utils import timezone
from datetime import timedelta


class ReportTestCase(TestCase):
    """Tests for the report model."""

    def setUp(self):  # noqa
        self.agreement = Agreement.objects.create(
            number=1,
            name="Name name",
            personnummer="980101-3039",
            phonenumber="0733221122",
            email="mail@mail.se",
            expires=timezone.now() + timedelta(days=365)
        )

        # Add some groups
        self.group1 = JournalEntryGroup.objects.create(
            name="Gruppen",
            main_group='lg_and_board',
        )
        self.group2 = JournalEntryGroup.objects.create(
            name="Sektionen",
            main_group='sections',
        )
        self.group3 = JournalEntryGroup.objects.create(
            name="Cool grupp",
            main_group='lg_and_board',
        )
        self.group4 = JournalEntryGroup.objects.create(
            name="Gruppen",
            main_group='other_officials',
        )

        # Add some journal entries
        self.first_entry = JournalEntry.objects.create(
            agreement=self.agreement, group=self.group1,
            meter_start=50, meter_stop=70
        )
        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group4,
            meter_start=70, meter_stop=75
        )
        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group2,
            meter_start=75, meter_stop=90
        )
        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group3,
            meter_start=100, meter_stop=124
        )
        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group1,
            meter_start=124, meter_stop=132
        )
        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group2,
            meter_start=132, meter_stop=157
        )

    # Test create a report
    def test_create_report(self):
        """Test creating a report."""
        first, last, _ = Report.get_new_report_details()
        report = Report.objects.create(first=first, last=last, cost_per_mil=20)
        self.assertEqual(report.first, self.first_entry.created)
        self.assertEqual(report.get_entries().count(), 6)

    def test_create_two_reports(self):
        """Test creating a report when a report already exists."""
        first, last, _ = Report.get_new_report_details()
        Report.objects.create(first=first, last=last, cost_per_mil=20)

        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group4,
            meter_start=157, meter_stop=169
        )

        JournalEntry.objects.create(
            agreement=self.agreement, group=self.group3,
            meter_start=169, meter_stop=179
        )

        first, last, _ = Report.get_new_report_details()
        previous_report = Report.get_latest_report()
        report = Report.objects.create(first=first, last=last, cost_per_mil=20)

        self.assertEqual(report.first, previous_report.last)
        self.assertEqual(report.get_entries().count(), 2)

    # Test calculation functions
    def test_statistics_for_groups(self):
        """Test that statisitcs for groups are correct."""
        first, last, _ = Report.get_new_report_details()
        report = Report.objects.create(first=first, last=last, cost_per_mil=20)

        statistics = report.get_statistics_for_groups()

        # Manually calculated from journal entries in setup
        kilometers_for_groups = {
            self.group1.pk: 28,
            self.group2.pk: 40,
            self.group3.pk: 24,
            self.group4.pk: 5
        }

        mil_for_groups = {
            self.group1.pk: 3,
            self.group2.pk: 4,
            self.group3.pk: 3,
            self.group4.pk: 1
        }

        cost_for_groups = {
            self.group1.pk: 60,
            self.group2.pk: 80,
            self.group3.pk: 60,
            self.group4.pk: 20
        }

        for statistic in statistics:
            expected_kilometers = kilometers_for_groups[statistic['group'].pk]
            actual_kilometers = statistic['kilometers']
            self.assertEqual(expected_kilometers, actual_kilometers)

            expected_mil = mil_for_groups[statistic['group'].pk]
            actual_mil = statistic['mil']
            self.assertEqual(expected_mil, actual_mil)

            expected_cost = cost_for_groups[statistic['group'].pk]
            actual_cost = statistic['cost']
            self.assertEqual(expected_cost, actual_cost)

    def test_lost_cost(self):
        """Test calculation of lost cost."""
        first, last, _ = Report.get_new_report_details()
        report = Report.objects.create(first=first, last=last, cost_per_mil=20)

        lost_cost = report.calculate_lost_cost()
        self.assertEqual(lost_cost['difference'], 10),
        self.assertEqual(lost_cost['lost_cost'], 20)
