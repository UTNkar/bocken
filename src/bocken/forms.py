from django.forms import ModelForm, NumberInput, TextInput, BooleanField
from .models import JournalEntry


class JournalEntryForm(ModelForm):
    """The modelform for journal entries."""

    confirm = BooleanField(
        required=True,
        label='Jag intygar att bocken är i gott skick'
    )

    class Meta:
        model = JournalEntry
        fields = [
            'agreement_number', 'name', 'group', 'meter_start', 'meter_stop'
        ]
        widgets = {
            # Agreement number should be entered manually to make it more
            # difficult for people to use another person's agreement number
            "agreement_number": NumberInput(
                attrs={'placeholder': 'Avtalsnummer'}
            ),
            "name": TextInput(
                attrs={'placeholder': 'Namn'}
            ),
            "meter_start": TextInput(
                attrs={'placeholder': 'Mätare vid start'}
            ),
            "meter_stop": TextInput(
                attrs={'placeholder': 'Mätare vid stopp'}
            ),
        }
        labels = {
            'agreement_number': 'file',
            'name': 'user',
            'group': 'users',
            'meter_start': 'play-circle',
            'meter_stop': 'stop-circle',
        }
