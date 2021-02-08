from django.forms import ModelForm, TextInput, BooleanField, CharField
from django.core.exceptions import ValidationError
from .models import JournalEntry, Agreement
from .validators import validate_personnummer


class JournalEntryForm(ModelForm):
    """The modelform for journal entries."""

    personnummer = CharField(
        required=True,
        validators=[validate_personnummer],
        label='user',
        widget=TextInput(attrs={
            'placeholder': 'YYYYMMDD-XXXX',
        }),
    )

    confirm = BooleanField(
        required=True,
        label='Jag intygar att bocken är i gott skick'
    )

    class Meta:
        model = JournalEntry
        fields = [
            'personnummer', 'group', 'meter_start', 'meter_stop'
        ]
        widgets = {
            "meter_start": TextInput(
                attrs={
                    'placeholder': 'Mätare vid start',
                    'autocomplete': "off"
                }
            ),
            "meter_stop": TextInput(
                attrs={
                    'placeholder': 'Mätare vid stopp',
                    'autocomplete': "off"
                }
            ),
        }
        labels = {
            'group': 'users',
            'meter_start': 'play-circle',
            'meter_stop': 'stop-circle',
        }
        help_texts = {
            'personnummer': "Ditt personnummer",
            'group': (
                "Är du osäker på vilken grupp du ska välja? "
                "Välj den grupp som känns rimligast att betala för din resa."
            ),
            'meter_start': (
                'Mätare vid start fylls i automatiskt från den senaste '
                'inlägget. Om siffran inte stämmer, fyll i det värdet '
                'som mätaren hade när du började köra samt kontakta '
                'UTN:s klubbmästare.'
            ),
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
        try:
            agreement = Agreement.objects.get(
                personnummer=self.cleaned_data['personnummer']
            )
            self.instance.agreement = agreement
        except Agreement.DoesNotExist:
            raise ValidationError("You don't have a written agreement")
