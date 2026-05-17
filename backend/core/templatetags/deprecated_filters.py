# core/templatetags/deprecated_filters.py
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def length_is(value, arg):
    """Replacement for deprecated length_is filter"""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

@register.filter
def length_is_list(value, arg):
    """For lists and other sequences"""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False