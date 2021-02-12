def personnummer_is_t_number(personnummer):
    """Check if the given personnummer is a t-number."""
    # If the first digit in the 4 last digits in a personnummer is
    # one of the following letters, the personnummer is a t-number.
    # These letters are the only ones that are allowed in a t-number.
    return personnummer[-4].upper() in [
        'T', 'R', 'S', 'U', 'W', 'X',
        'J', 'K', 'L', 'M', 'N'
    ]
