from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .models import JournalEntry
from .forms import JournalEntryForm


class JournalEntryCreate(CreateView):
    """The view for creating a journal entry."""

    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journalentry_create.html'
    success_url = reverse_lazy('add-entry-success')

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
    template_name = 'journalentry_create_success.html'
