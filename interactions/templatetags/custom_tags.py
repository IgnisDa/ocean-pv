import random

from django import template


register = template.Library()


@register.simple_tag(name='random_color')
def random_color():
    colors = ['success', 'danger', 'info', 'warning']
    return random.choice(colors)
