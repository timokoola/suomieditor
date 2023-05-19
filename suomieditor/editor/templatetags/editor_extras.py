from django import template
from django.template.defaultfilters import stringfilter

from editor.constants import EXAMPLE_NOUN_FORMS

register = template.Library()


# create a custom filter for help text
@register.filter("help_text")
@stringfilter
def help_text_filter(value):
    """Filter for help text."""
    return ", ".join(EXAMPLE_NOUN_FORMS[value])
