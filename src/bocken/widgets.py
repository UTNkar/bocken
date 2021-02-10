from django.forms.widgets import Select
from .constants import JOURNAL_ENTRY_ALL_GROUPS


class TwoLevelSelect(Select):
    template_name = 'two_level_select.html'

    def get_context(self, name, value, attrs):
        context = super(TwoLevelSelect, self).get_context(name, value, attrs)
        context['groups'] = JOURNAL_ENTRY_ALL_GROUPS

        groups_verbose_names = {}
        for key, main_group in JOURNAL_ENTRY_ALL_GROUPS.items():
            verbose_names = []
            for group in main_group['groups']:
                verbose_names.append(group[1])
            groups_verbose_names[key] = sorted(verbose_names)

        context['groups_verbose_names'] = groups_verbose_names
        return context
