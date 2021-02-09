from django.forms.widgets import Select


class TwoLevelSelect(Select):
    template_name = 'two_level_select.html'
