from django.forms import ModelForm, TextInput, BooleanField, CharField
from django.core.exceptions import ValidationError
from .models import JournalEntry, Agreement
from .validators import validate_personnummer
from .widgets import TwoLevelSelect
from django.utils.translation import gettext as _
from personnummer import personnummer


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
            )
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

        # If there is data from the previous form (a.k.a. invalid data
        # was passed) we need to add some of that data to the TwoLevelSelect
        # widget so that it can automatically choose a default option.
        # The widget is not capable of doing this on it's own since it does
        # not have access to the context of the form
        if 'data' in kwargs:
            form_data = kwargs.get('data')

            self.fields['group'].widget = TwoLevelSelect(
                initial_group=form_data.get('group'),
                initial_main_group=form_data.get("main-group")
            )
        else:
            self.fields['group'].widget = TwoLevelSelect()

    def clean_personnummer(self):
        """
        Get the agreement associated to the provided personnummer.

        The agreement is added to the instance.
        """
        try:
            pn = personnummer.parse(self.cleaned_data['personnummer'])
            # Format the personnummer into the long format
            return pn.format(True)
        except personnummer.PersonnummerException:
            # This exception occurs if the personnummer is a t-number.
            # All logic regarding the t-numbers are handled in the
            # personnummer validator so here we just return the personnummer.
            return self.cleaned_data['personnummer']

    def clean_meter_start(self):
        """Meter start must be larger than the meter stop in the last entry."""
        latest_entry = JournalEntry.get_latest_entry()
        if latest_entry.meter_stop > self.cleaned_data['meter_start']:
            raise ValidationError(_(
                "Trip meter at start must be larger "
                "than the last entry in the journal"
            ) + ': {0} km'.format(latest_entry.meter_stop))

        return self.cleaned_data['meter_start']

    def clean(self): # noqa
        cleaned_data = super(JournalEntryForm, self).clean()

        # Find the corresponding agreement. If the personnummer is not
        # availble it means that the personnummer is invalid. In that case
        # we don't need to add an error message that a user does not
        # have a written agreement.
        person_nummer = self.cleaned_data.get('personnummer')
        if person_nummer:
            try:
                agreement = Agreement.objects.get(
                    personnummer=person_nummer
                )
                self.instance.agreement = agreement
            except Agreement.DoesNotExist:
                self.add_error('personnummer', _(
                    "You don't have a written agreement which you must have "
                    "to drive bocken. Contact the head of the pub crew and "
                    "send a copy of the details you wrote into the fields "
                    "below."
                ))

        # Make sure meter stop is larger than meter start
        meter_start = cleaned_data.get('meter_start', 0)
        if cleaned_data['meter_stop'] <= meter_start:
            self.add_error('meter_stop', _(
                "Trip meter at stop must be larger than the trip meter at "
                "start"
            ))

        return cleaned_data
