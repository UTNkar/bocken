from django.forms import Form, CharField
from bocken.validators import validate_personnummer


class AgreementExpireForm(Form):
    personnummer = CharField(
        required=True,
        validators=[validate_personnummer]
    )
