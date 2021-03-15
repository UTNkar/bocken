from django.forms.widgets import Select
from bocken.models import JournalEntryGroup


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

    def get_context(self, name, value, attrs):
        """Provide all the groups and initial values to the template."""
        context = super(TwoLevelSelect, self).get_context(name, value, attrs)

        groups = {}

        all_main_groups = JournalEntryGroup._meta.\
            get_field('main_group').choices
        all_groups = JournalEntryGroup.objects.all()

        for main_group, verbose_name in all_main_groups:
            # Get a list of the names of all groups that belong to the current
            # main group
            groups_in_main_group = all_groups.filter(
                main_group=main_group
            ).values_list('id', "name")

            # Sort the groups alphabetically
            sorted_groups = sorted(
                groups_in_main_group,
                key=lambda element: element[1]
            )

            groups[str(verbose_name)] = sorted_groups

        # Groups will have the following structure:
        # {
        #   'Committees': ['committee1', 'committee2'],
        #   'Sections': ['section1', 'section2'],
        #    ...
        # }
        context['groups'] = groups
        context['all_main_groups'] = all_main_groups

        context['initial_group'] = self.initial_group
        context['initial_main_group'] = self.initial_main_group

        return context
