from django.forms.widgets import Select
from .constants import JOURNAL_ENTRY_ALL_GROUPS


class TwoLevelSelect(Select):
    """
    A select widget that consists of two selects.

    Two level select divides all groups for journal entries into main
    groups to make it more easy to find a specific group. Each group
    has been placed into a main group. When a main group is selected
    the groups that can be selected is limited to the groups belonging
    """

    template_name = 'two_level_select.html'

    def get_context(self, name, value, attrs):
        """Provide all the groups and all the verbose names for the groups."""
        context = super(TwoLevelSelect, self).get_context(name, value, attrs)
        context['groups'] = JOURNAL_ENTRY_ALL_GROUPS

        # Creates arrays with all verbose names for each main group
        groups_verbose_names = {}
        for key, main_group in JOURNAL_ENTRY_ALL_GROUPS.items():
            verbose_names = []
            for group in main_group['groups']:
                verbose_names.append(group[1])
            groups_verbose_names[key] = sorted(verbose_names)

        context['groups_verbose_names'] = groups_verbose_names
        return context
