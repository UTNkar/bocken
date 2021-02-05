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
