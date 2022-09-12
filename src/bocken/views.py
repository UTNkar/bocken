from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from bocken.forms import AgreementExpireForm
from .models import JournalEntry
from .forms import JournalEntryForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import mail_admins
from django.utils.timezone import localtime, now


class JournalEntryCreate(CreateView):
    """The view for creating a journal entry."""

    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journalentry_create.html'
    success_url = reverse_lazy('add-entry-success')

    def form_valid(self, form):
        """Handle when a form submission was valid."""
        agreement = form.instance.agreement
        if agreement.has_expired():
            messages.warning(
                self.request,
                _(
                    "Your agreement has expired! The journal entry you just "
                    "created has been saved but you need to renew your "
                    "agreement. Contact UTN:s Head of The Pubcrew: "
                    "<a class='text-blue-700' "
                    "href='mailto:%(email)s'>"
                    "%(email)s</a>"
                ) % {'email': settings.KLUBBMASTARE_EMAIL},
                extra_tags="safe"
            )
            mail_admins(
                "Expired agreement",
                '{}, personnummer: {}, added a journal entry but their '
                'agreement has expired. Please contact them to update '
                'their agreement.'.format(
                    agreement.name,
                    agreement.personnummer
                ),
                fail_silently=True
            )

        # Check if a gap has occured
        latest_entry = JournalEntry.get_latest_entry()
        if latest_entry:
            previous_meter_stop = latest_entry.meter_stop
            if form.cleaned_data['meter_start'] > previous_meter_stop:
                mail_admins(
                    "A gap has occured",
                    (
                        "A journal entry was added by {} at {} which created "
                        "a gap between the two latest journal entries. In "
                        "order to avoid lost costs this needs to be "
                        "investigated and fixed."
                    ).format(
                        form.instance.agreement.name,
                        localtime(now()).strftime("%Y-%m-%d %H:%M")
                    ),
                    fail_silently=True
                )

        return super(JournalEntryCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle when a post request comes to this view.

        Since the main group in the two level select is not a field on the
        model, django does not automatically add it to the forms data. This has
        to be done manually via this view since this is the only place where
        we can access the main group.
        """
        self.main_group = request.POST.get("main-group")
        return super(JournalEntryCreate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add extra context to the view.

        This makes the main group available in the JournalEntryForm
        and adds the three latest entries to the context.
        """
        context = super(CreateView, self).get_context_data(**kwargs)

        # On get requests, there is no main group
        if hasattr(self, 'main_group'):
            context['main_group'] = self.main_group

        context['three_latest_entries'] = \
            JournalEntry.get_three_latest_entries()

        return context


class JournalEntryCreateSuccess(TemplateView):
    """The success view when a valid journal entry was submitted."""

    template_name = 'journalentry_create_success.html'


class StartPage(FormView):
    """The start page."""

    form_class = AgreementExpireForm
    template_name = 'start_page.html'
    success_url = reverse_lazy('start-page')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)
