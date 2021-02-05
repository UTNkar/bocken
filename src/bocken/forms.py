from django.forms import ModelForm, TextInput, BooleanField, CharField
from .models import JournalEntry
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
                attrs={'placeholder': 'Mätare vid start'}
            ),
            "meter_stop": TextInput(
                attrs={'placeholder': 'Mätare vid stopp'}
            ),
        }
        labels = {
            'group': 'users',
            'meter_start': 'play-circle',
            'meter_stop': 'stop-circle',
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
