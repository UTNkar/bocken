from django.forms import ModelForm, ValidationError
from bocken.models.journal_entry import JournalEntry
from bocken.models.report import Report
from django.utils.translation import gettext_lazy as _


class ReportForm(ModelForm):
    """
    Form for creating a report in the admin pages.

    First and last are created automatically while cost per mil is set in
    the form.
    """

    class Meta:
        model = Report
        fields = ['cost_per_mil']

    def clean(self):  # noqa
        super(ReportForm, self).clean()

        # If there is no primary key on the instance we are creating
        # a new report
        if not self.instance.pk:
            if not JournalEntry.entries_exists():
                raise ValidationError(
                    _(
                        "Can not create a report because "
                        "there are no journal entries"
                    )
                )

            first, last, entries = Report.get_new_report_details()

            if entries:
                self.instance.first = first
                self.instance.last = last
            else:
                raise ValidationError(
                    _(
                        "Can not create a report because there are no "
                        "journal entries between these two timestamps"
                    )
                )
