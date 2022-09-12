from django.forms import EmailField, FileField, ModelForm
from django.utils.translation import gettext_lazy as _
from bocken.models.agreement import Agreement


class AgreementForm(ModelForm):
    """A form for agreements."""

    # Email is set to required in this form so that new agreements
    # are created with emails. TODO: When all agreements have an email
    # this can be removed and the agreement model can be changed as well.
    email = EmailField(
        required=True,
        help_text=_(
            "The person's private email. Should not be an email ending in "
            "@utn.se."
        ),
    )

    agreement_file = FileField(
        required=True,
        label=_("Signed agreement"),
    )

    class Meta:
        model = Agreement
        fields = [
            'name', 'personnummer', 'phonenumber',
            'email', 'agreement_file', 'expires'
        ]
