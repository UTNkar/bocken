from django.forms import ModelForm, TextInput, BooleanField, CharField
from django.core.exceptions import ValidationError
from .models import JournalEntry, Agreement
from .validators import validate_personnummer
from .widgets import TwoLevelSelect
from django.utils.translation import gettext as _


class JournalEntryForm(ModelForm):
    """The modelform for journal entries."""

    personnummer = CharField(
        required=True,
        validators=[validate_personnummer],
        label='user',
        widget=TextInput(attrs={
            'placeholder': 'YYYYMMDD-XXXX',
        }),
        help_text=_("Your personnummer")
    )

    confirm = BooleanField(
        required=True,
        label=_("I confirm that Bocken is clean and in good shape")
    )

    class Meta:
        model = JournalEntry
        fields = [
            'personnummer', 'group', 'meter_start', 'meter_stop'
        ]
        widgets = {
            "meter_start": TextInput(
                attrs={
                    'placeholder': _("Trip meter at start"),
                    'autocomplete': "off",
                    'inputmode': 'numeric'
                }
            ),
            "meter_stop": TextInput(
                attrs={
                    'placeholder': _("Trip meter at stop"),
                    'autocomplete': "off",
                    'inputmode': 'numeric'
                }
            ),
            "group": TwoLevelSelect(),
        }
        labels = {
            'group': 'users',
            'meter_start': 'play-circle',
            'meter_stop': 'stop-circle',
        }
        help_texts = {
            'group': _(
                "Not sure which group to choose? Choose the group that seems "
                "most reasonable to be paying for your trip."
            ),
            'meter_start': _(
                "Trip meter at start is filled in automatically from the "
                "latest entry. If the number is not correct, enter the value "
                "that the meter had when you started driving. Also inform the "
                "head of the pub crew about this."
            )
        }

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)
        # Set the initial value for the meter start to the stop value of the
        # last entry since it most likely is the value of the meter when a
        # person starts driving.
        latest_entry = JournalEntry.get_latest_entry()
        if latest_entry:
            self.initial = {
                'meter_start': latest_entry.meter_stop
            }

    def clean_personnummer(self):
        """
        Get the agreement associated to the provided personnummer.

        The agreement is added to the instance.
        """
        try:
            agreement = Agreement.objects.get(
                personnummer=self.cleaned_data['personnummer']
            )
            self.instance.agreement = agreement
        except Agreement.DoesNotExist:
            raise ValidationError(_("You don't have a written agreement"))
