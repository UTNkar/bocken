from django import template
from bocken.utils import kilometers_to_mil

register = template.Library()


@register.simple_tag(takes_context=True)
def calculate_lost_cost(
    context, total_driven_kilometers, total_logged_kilometers
):
    """
    Calculate the lost cost in a report.

    Returns a dict with the difference between the driven and logged kilometers
    {
        'difference': The difference (int),
        'lost_cost': The lost cost (kr)
    }
    """
    total_driven_kilometers = int(total_driven_kilometers)
    total_logged_kilometers = int(total_logged_kilometers)

    difference = total_driven_kilometers - total_logged_kilometers

    report = context['original']
    mil = kilometers_to_mil(difference)

    lost_cost = report.calculate_total_cost(mil)
    return {
        'difference': difference,
        'lost_cost': lost_cost
    }
