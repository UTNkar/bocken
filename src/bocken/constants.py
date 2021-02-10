from django.utils.translation import gettext as _

# All groups have been divided into main groups to make it easier to find
# a specific group. Each main group has a verbose name and the groups belonging
# to that main group, represented as an array. Each group is represented as a
# tuple where the first element is the computer name i.e. the name django
# will use when storing a group in the database.
# The second element is the string that the user will see in the form.
# This mimics django's behaviour of choices.
JOURNAL_ENTRY_GROUPS = {
    'committees_workgroups': {
        'verbose_name': _("UTN's committees and workgroups"),
        'groups': [
            ('td', _('TD'))
        ]
    },
    'lg_and_board': {
        'verbose_name': _("UTN's management team and board"),
        'groups': [
            ('board', _('Board'))
        ]
    },
    'fum': {
        'verbose_name': _("FUM"),
        'groups': [
            ('tmp', _('TMP'))
        ]
    },
    'other_officials': {
        'verbose_name': _("Other officials within UTN"),
        'groups': [
            ('head_of_administrations', _('Head of administrations'))
        ]
    },
    'sections': {
        'verbose_name': _("Sections"),
        'groups': [
            ('dv', _('DV'))
        ]
    },
    'cooperations': {
        'verbose_name': _("Cooperations"),
        'groups': [
            ('best', _('BEST'))
        ]
    },
}
