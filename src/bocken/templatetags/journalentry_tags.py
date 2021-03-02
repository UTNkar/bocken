from django import template
from ..models import Report, JournalEntry

register = template.Library()


@register.simple_tag
def get_new_report_range():
    """
    Return the range of journal entries that will be added in new report.

    If a range can not be created, an error message is returned is instead.
    """
    first = Report.get_first_journal_entry_not_in_report()
    last = JournalEntry.get_latest_entry()
    if first and last:
        return "{} - {}".format(
            first.created_formatted,
            last.created_formatted
        )
    else:
        # TODO: Make better error message
        return "Can not create"
