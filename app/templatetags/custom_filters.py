from django import template

register = template.Library()

@register.filter
def getattr(obj, attr):
    return getattr(obj, attr)
from django import template


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr)

