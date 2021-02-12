from django.utils.translation import gettext as _

# All groups have been divided into main groups to make it easier to find
# a specific group. Each main group has a verbose name and the groups belonging
# to that main group, represented as an array. Each group is represented as a
# tuple where the first element is the computer name i.e. the name django
# will use when storing a group in the database.
# The second element is the string that the user will see in the form.
# This mimics django's behaviour of choices.

JOURNAL_ENTRY_COMMITTEES_WORKGROUPS = [
    ('baska', 'Baskå'),
    ('td', 'TD'),
    ('proppen', 'Proppen'),
    ('kv', 'KV'),
    ('rebusrallyt', 'Rallykå'),
    ('balen', 'Balkå'),
    ('cafegruppen', 'Cafegruppen'),
    ('forska', 'Forskå'),
    ('eventgruppen', 'Eventgruppen'),
    ('exka', 'Examenkå'),
    ('marknadsforingsgruppen', 'Marknadsföringsgruppen'),
    ('mer', 'MER'),
    ('utnarm', 'Utnarm'),
    ('polhacks', 'Polhackskå'),
    ('dka', 'Dkå'),
    ('karhusgruppen', 'Kårhusgruppen'),
    ('techna', 'Techna')
]

JOURNAL_ENTRY_LG_AND_BOARD = [
    ('board', 'Styrelsen'),
    ('utbex', 'Utb-ex'),
    ('utbn', 'Utb-n'),
    ('utbt', 'Utb-t'),
    ('soc', 'Soc'),
    ('int', 'Int'),
    ('na', 'NA'),
    ('plutnarm', 'PL Utnarm'),
    ('ordf', 'Ordförande'),
    ('viceordf', 'Vice Ordförande')
]

JOURNAL_ENTRY_FUM = [
    ('tmp', 'TMP'),
    ('valberedningen', 'Valberedningen')
]

JOURNAL_ENTRY_OTHER_OFFICIALS = [
    ('forvaltning', 'Förvaltning'),
    ('historiograf', 'Historiograf'),
    ('pelarmarskalk', 'Pelarmarskalk'),
    ('internrevisorer', 'Internrevisorer')
]

JOURNAL_ENTRY_SECTIONS = [
    ('bas', 'BAS'),
    ('dv', 'DV'),
    ('e', 'E'),
    ('es', 'ES'),
    ('f', 'F'),
    ('h', 'H'),
    ('i', 'I'),
    ('it', 'IT'),
    ('k', 'K'),
    ('nvb', 'NVB (BÄR)'),
    ('nvf', 'NVF (FysKam)'),
    ('nvg', 'NVG (GRUS)'),
    ('nvk', 'NVK (IUPAK)'),
    ('nvl', 'NVL (LärNat)'),
    ('nvm', 'NVM (Moebius)'),
    ('q', 'Q'),
    ('sts', 'STS'),
    ('w', 'W'),
    ('x', 'X'),
]

JOURNAL_ENTRY_COOPERATINS = [
    ('best', 'BEST'),
    ('teknatspex', 'Teknat Spex'),
    ('genius', 'Genius'),
    ('iaeste', 'IAESTE'),
    ('ibk', 'IBK'),
    ('igem', 'IGEM'),
    ('siv', 'SIV'),
    ('mfk', 'MFK'),
    ('gb', 'GB')
]

JOURNAL_ENTRY_ALL_GROUPS = {
    'committees_workgroups': {
        'verbose_name': _("UTN's committees and workgroups"),
        'groups': JOURNAL_ENTRY_COMMITTEES_WORKGROUPS
    },
    'lg_and_board': {
        'verbose_name': _("UTN's management team and board"),
        'groups': JOURNAL_ENTRY_LG_AND_BOARD
    },
    'fum': {
        'verbose_name': _("FUM"),
        'groups': JOURNAL_ENTRY_FUM
    },
    'other_officials': {
        'verbose_name': _("Other officials within UTN"),
        'groups': JOURNAL_ENTRY_OTHER_OFFICIALS
    },
    'sections': {
        'verbose_name': _("Sections"),
        'groups': JOURNAL_ENTRY_SECTIONS
    },
    'cooperations': {
        'verbose_name': _("Cooperations"),
        'groups': JOURNAL_ENTRY_COOPERATINS
    },
}
