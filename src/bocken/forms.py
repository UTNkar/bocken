from django.forms import ModelForm, NumberInput
from .models import JournalEntry


class JournalEntryForm(ModelForm):
    """The modelform for journal entries."""

    class Meta:
        model = JournalEntry
        fields = [
            'agreement_number', 'name', 'group', 'meter_start', 'meter_stop'
        ]
        widgets = {
            # Agreement number should be entered manually to make it more
            # difficult for people to use another person's agreement number
            "agreement_number": NumberInput()
        }
        labels = {
            'agreement_number': 'file',
            'name': 'user',
            'group': 'users',
            'meter_start': 'play-circle',
            'meter_stop': 'stop-circle',
        }
