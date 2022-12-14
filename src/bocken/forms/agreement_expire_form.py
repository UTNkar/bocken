from django.forms import Form, CharField, TextInput
from bocken.utils import format_personnummer
from bocken.validators import validate_personnummer
from django.utils.translation import gettext_lazy as _


class AgreementExpireForm(Form):
    personnummer = CharField(
        required=True,
        validators=[validate_personnummer],
        label='user',
        widget=TextInput(attrs={
            'placeholder': 'YYYYMMDD-XXXX',
        }),
        help_text=_("Your personnummer"),
        min_length=10,  # Shortest format is 10 characters long
        max_length=13  # Longest format is 13 characters long
    )

    def clean_personnummer(self):
        """Format the personnummer to the correct format."""
        return format_personnummer(self.cleaned_data['personnummer'])
