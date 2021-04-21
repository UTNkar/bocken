from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def calculate_lost_cost(context):
    """
    Calculate the lost cost in a report.

    Returns a dict with the difference between the driven and logged kilometers
    {
        'difference': The difference (int),
        'lost_cost': The lost cost (kr)
    }
    """
    return context['original'].calculate_lost_cost()
