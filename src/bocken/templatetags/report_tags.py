from django import template
from ..models import Report

register = template.Library()


@register.simple_tag
def get_new_first():
    return Report.get_first_for_new_report()
