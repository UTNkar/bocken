from bocken.models.agreement import Agreement
from bocken.models.journal_entry import JournalEntry
from bocken.models.vehicle import Vehicle
from ..validators import validate_personnummer
from ..utils import format_personnummer
from ..widgets import TwoLevelSelect
from captcha.fields import ReCaptchaField
from django.forms import (
    ModelForm, TextInput, BooleanField, CharField, CheckboxInput,
    ValidationError
)
from django.utils.translation import gettext_lazy as _


class JournalEntryForm(ModelForm):
    """The modelform for journal entries."""

    personnummer = CharField(
        required=True,
        validators=[validate_personnummer],
        label='user',
        widget=TextInput(attrs={
            'placeholder': 'YYYYMMDDXXXX',
        }),
        help_text=_("Your personnummer")
    )

    confirm = BooleanField(
        required=True,
        label=_("I confirm that the vehicle is clean and in good shape"),
        widget=CheckboxInput(attrs={'class': 'h-8 w-8'})
    )

    captcha = ReCaptchaField()

    class Meta:
        model = JournalEntry
        fields = [
            'personnummer', 'vehicle', 'group', 'meter_start', 'meter_stop'
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
            'vehicle': 'truck'
        }
        help_texts = {
            'group': _(
                "Not sure which group to choose? Choose the group that seems "
                "most reasonable to be paying for your trip."
            ),
            'meter_start': _(
                "Trip meter at start is filled in automatically from the "
                "latest entry. If the number is not correct, enter the value "
                "that the meter had when you started driving. Also inform "
                "UTN:s Union House Manager about this."
            'vehicle': _(
                "Choose the type of vehicle you have driven."
            )
        }

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)
        # Set the initial value for the meter start to the stop value of the
        # last entry based on the current vehicle choice since it most
        # likely is the value of the meter when a person starts driving.
        all_vehicles = Vehicle.objects.all()
        latest_entries = [
            JournalEntry.get_latest_entry(x)
            for x in all_vehicles
            if JournalEntry.get_latest_entry(x) is not None
        ]
        if latest_entries:
            latest_entry = latest_entries[0]
            self.initial = {
                'meter_start': latest_entry.meter_stop,
            }
            # This stores all of the latest registered trips for vehicle.
            # By doing this we can hence "support" any amount of vehicle
            # and fetch their latest trip to automatically set as
            # a value for when a user is registering a new journal entry
            for item in latest_entries:
                self.initial[
                    f'meter_start_{str(item.vehicle.id)}'
                ] = item.meter_stop
        else:
            # if there is not a latest entry, then fetch from vehicle objects
            # ideally it should always be fetched from here but..?
            for vehicle in all_vehicles:
                self.initial[
                    f'meter_start_{str(vehicle.id)}'
                ] = vehicle.vehicle_meter_stop
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
        """Format the personnummer to the correct format."""
        return format_personnummer(self.cleaned_data['personnummer'])

    def clean_meter_start(self):
        """Meter start must be larger than the meter stop in the last entry."""
        form_vehicle = self.cleaned_data['vehicle']
        latest_entry = JournalEntry.get_latest_entry(form_vehicle)
        if latest_entry:
            if latest_entry.meter_stop > self.cleaned_data['meter_start']:
                raise ValidationError(_(
                    "Trip meter at start must be larger "
                    "than the last entry in the journal"
                ) + ': {0} km'.format(latest_entry.meter_stop))

        return self.cleaned_data['meter_start']

    def clean(self):  # noqa
        cleaned_data = super(JournalEntryForm, self).clean()

        # Find the corresponding agreement. If the personnummer is not
        # availble it means that the personnummer is invalid. In that case
        # we don't need to add an error message that a user does not
        # have a written agreement.
        person_nummer = self.cleaned_data.get('personnummer')
        veh = self.cleaned_data.get('vehicle')
        if person_nummer:
            try:
                agreement = Agreement.objects.get(
                    personnummer=person_nummer
                )
                can_use_car = agreement.car_agreement
                can_use_bike = agreement.bike_agreement
                if veh.car:
                    if not can_use_car:
                        self.add_error('vehicle', _(
                            "You don't have a written agreement which you "
                            "must have to drive a car. Contact the head of "
                            "the pub crew and send a copy of the details "
                            "you wrote inte the fields below."
                        ))
                else:
                    if not can_use_bike:
                        self.add_error('vehicle', _(
                            "You don't have a written agreement which you "
                            "must have to drive a bike. Contact the head of "
                            "the pub crew and send a copy of the details "
                            "you wrote inte the fields below."
                        ))

                self.instance.agreement = agreement
            except Agreement.DoesNotExist:
                self.add_error('personnummer', _(
                    "You don't have a written agreement which you "
                    "must have to drive a vehicle. Contact the Union "
                    "House Manager and send a copy of the details "
                    "you wrote inte the fields below."
                ))

        # Make sure meter stop is larger than meter start
        meter_start = cleaned_data.get('meter_start', 0)
        meter_stop = cleaned_data['meter_stop']
        if cleaned_data['meter_stop'] <= meter_start:
            self.add_error('meter_stop', _(
                "Trip meter at stop must be larger than the trip meter at "
                "start"
            ))
        else:
            if veh:
                Vehicle.objects.filter(id=veh.id).update(
                    vehicle_meter_start=meter_start,
                    vehicle_meter_stop=meter_stop
                )
        return cleaned_data
