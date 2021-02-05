from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import JournalEntry
from .forms import JournalEntryForm


class JournalEntryCreate(CreateView):
    """The view for creating a journal entry."""

    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journalentry_create.html'
    success_url = reverse_lazy('add-entry')
