from django.views.generic.edit import CreateView
from .models import JournalEntry
from .forms import JournalEntryForm


class JournalEntryCreate(CreateView):
    """The view for creating a journal entry."""

    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journalentry_create.html'
