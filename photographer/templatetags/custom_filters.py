from django import template

register = template.Library()

@register.filter
def is_equal(value, arg):
    return value == arg
