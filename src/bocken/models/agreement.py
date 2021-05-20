from django.db import models
from bocken.validators import validate_phonenumber, validate_personnummer
from ..utils import format_personnummer
from ..fields import PhonenumberField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta
from django.utils.html import format_html
from django.template.defaultfilters import date
from django.core.mail import send_mass_mail
from django.conf import settings


def get_default_expires():
    """Return the default expires date for an agreement."""
    return now().date() + timedelta(days=365)


class Agreement(models.Model):
    """
    Represents a person who has signed a bocken-agreement.

    When a person has signed a bocken-agreement they can drive bocken
    for 1 year. After that year they have to sign a new agreement.
    """

    name = models.CharField(
        max_length=120,
        verbose_name=_("Name"),
        help_text=_("First and last name")
    )

    personnummer = models.CharField(
        max_length=13,
        validators=[validate_personnummer],
        unique=True
    )

    phonenumber = PhonenumberField(
        max_length=20,
        validators=[validate_phonenumber],
        verbose_name=_("Phonenumber")
    )

    # Email is allowed to be blank since we don't have an email address to
    # everyone who has an agreement at the time of creation of this system.
    # TODO: Remove blank when there is an email address for all
    # agreements. Also make email unique=True at the same time
    email = models.EmailField(
        blank=True,
        help_text=_(
            "The person's private email. Should not be an email ending in "
            "@utn.se."
        ),
    )

    # agreement file is allowed to be blank since not everyone has signed the
    # latest agreement at the time of creation of this system. Instead of
    # scanning all those agreements, they will remain in their folder until
    # everyone has signed the new agreement.
    # TODO: Remove blank when everyone has an agreement file in the system
    agreement_file = models.FileField(
        upload_to='agreements/',
        verbose_name=_("Signed agreement"),
        blank=True
    )

    expires = models.DateField(
        verbose_name=_("Valid until"),
        default=get_default_expires,
        help_text=_("Agreements are valid for 1 year by default.")
    )

    class Meta:
        verbose_name = _("Agreement")
        verbose_name_plural = _("Agreements")
        ordering = ('name',)
        indexes = [
            models.Index(
                fields=['name', 'personnummer']
            )
        ]

    def __str__(self):  # noqa
        return "{} - {}".format(self.name, self.personnummer)

    def has_expired(self):
        """Check if an agreement has expired."""
        return self.expires <= now().date()

    def expires_colored(self):
        """
        Color the expires field red if the agreement has expired.

        This is used in the admin pages.
        """
        if self.has_expired():
            return format_html(
                (
                    '<p '
                    'style="background: rgb(220, 38, 38);'
                    'color: white; margin:0; padding:0;'
                    '">{}</p>'
                ),
                date(self.expires),  # Format the date correctly
            )
        else:
            return self.expires
    expires_colored.admin_order_field = 'expires'
    expires_colored.short_description = expires.verbose_name

    @staticmethod
    def send_renewal_reminder_10_days_left():
        """Send an email to all agreements that expire in 10 days."""
        agreements = Agreement.objects.filter(
            expires=now() + timedelta(days=10)
        )

        emails = agreements.exclude(email=None).values_list('email', flat=True)

        if len(emails) > 0:
            subject = _("Reminder to update your Bocken agreement")
            message = _(
                "This is an automated message from UTN:s journal system for "
                "Bocken. You are receiving this email because you have a "
                "Bocken agreement that will expire in 10 days. If you want "
                "to continue driving Bocken you must contact UTN:s "
                "klubbmästare by replying to this email.\n\n"
                "If you do not want to continue driving Bocken, you can "
                "ignore this email."
            )
            message_tuple = \
                subject, message, settings.KLUBBMASTARE_EMAIL, list(emails)
            send_mass_mail(
                (message_tuple, )
            )

    def save(self, *args, **kwargs):  # noqa
        self.personnummer = format_personnummer(self.personnummer)
        super(Agreement, self).save(*args, **kwargs)
