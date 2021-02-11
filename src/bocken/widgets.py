from django.forms.widgets import Select
from .constants import JOURNAL_ENTRY_ALL_GROUPS


class TwoLevelSelect(Select):
    """
    A select widget that consists of two selects.

    Two level select divides all groups for journal entries into main
    groups to make it more easy to find a specific group. Each group
    has been placed into a main group. When a main group is selected
    the groups that can be selected is limited to the groups belonging
    to that main group.
    """

    template_name = 'two_level_select.html'

    def get_context(self, name, value, attrs):
        """Provide all the groups to the template."""
        context = super(TwoLevelSelect, self).get_context(name, value, attrs)

        # Convert all list of tuples to list of lists since javascript
        # does not have tuples
        groups = JOURNAL_ENTRY_ALL_GROUPS
        for key, main_group in JOURNAL_ENTRY_ALL_GROUPS.items():
            groups_to_array = []
            for group in main_group['groups']:
                groups_to_array.append(list(group))
            groups[key]['groups'] = groups_to_array

        context['groups'] = groups
        return context
