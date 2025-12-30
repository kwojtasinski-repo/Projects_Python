from django import template

register = template.Library()

@register.filter
def js_bool(value):
    """
    Converts Python bool to JavaScript boolean literal.
    """
    return "true" if value else "false"
