from personnummer import personnummer as pn
from math import ceil
from django.utils.html import format_html


def personnummer_is_t_number(personnummer):
    """Check if the given personnummer is a t-number."""
    # If the first digit in the 4 last digits in a personnummer is
    # one of the following letters, the personnummer is a t-number.
    # These letters are the only ones that are allowed in a t-number.
    return personnummer[-4].upper() in [
        'T', 'R', 'S', 'U', 'W', 'X',
        'J', 'K', 'L', 'M', 'N'
    ]


def format_personnummer(personnummer):
    """
    Format personnummer into the long format.

    If personnummer is a T-number, no formating is done
    """
    try:
        parsed_personnummer = pn.parse(personnummer)
        # Format the personnummer into the long format
        return parsed_personnummer.format(True)
    except pn.PersonnummerException:
        # This exception occurs if the personnummer is a t-number.
        # All logic regarding the t-numbers are handled in the
        # personnummer validator so here we just return the personnummer.
        return personnummer


def kilometers_to_mil(kilometers: int):
    """
    Convert kilometers to mil.

    The result is rounded up since groups pay for every started mil.
    """
    return ceil(kilometers / 10)


def mark_admin_list_cell(value):
    """
    Mark a list cell in the admin pages by making the cell red.

    Returns the formatted list cell with the value provided
    """
    return format_html(
        (
            '<p '
            'style="background: rgb(220, 38, 38);'
            'color: white; margin:0; padding:0;'
            '">{}</p>'
        ),
        value,  # Format the date correctly
    )
