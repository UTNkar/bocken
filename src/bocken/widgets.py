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

    def __init__(
        self, attrs=None, initial_group=None, initial_main_group=None
    ):
        super(TwoLevelSelect, self).__init__()
        self.initial_group = initial_group
        self.initial_main_group = initial_main_group

    @staticmethod
    def _take_second(element):
        return element[1]

    def get_context(self, name, value, attrs):
        """Provide all the groups and initial values to the template."""
        context = super(TwoLevelSelect, self).get_context(name, value, attrs)

        # Convert all list of tuples to list of lists since javascript
        # does not have tuples
        groups = JOURNAL_ENTRY_ALL_GROUPS
        for key, main_group in JOURNAL_ENTRY_ALL_GROUPS.items():
            groups_to_array = []

            # Sort the groups based on their verbose name
            sorted_groups = sorted(
                main_group['groups'],
                key=TwoLevelSelect._take_second
            )

            for group in sorted_groups:
                groups_to_array.append(list(group))
            groups[key]['groups'] = groups_to_array

        context['groups'] = groups

        context['initial_group'] = self.initial_group
        context['initial_main_group'] = self.initial_main_group

        return context
