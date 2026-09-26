from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Returns the value turned into a list after splitting by key.
    Usage: {{ message.message|split:"|" }}
    """
    return value.split(key)