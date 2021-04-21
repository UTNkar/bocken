from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .models import JournalEntry
from .forms import JournalEntryForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import mail_admins


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
        Add the main group to the views context.

        This makes the main group available in the JournalEntryForm
        """
        context = super(CreateView, self).get_context_data(**kwargs)

        # On get requests, there is no main group
        if hasattr(self, 'main_group'):
            context['main_group'] = self.main_group

        return context


class JournalEntryCreateSuccess(TemplateView):
    """The success view when a valid journal entry was submitted."""

    template_name = 'journalentry_create_success.html'
