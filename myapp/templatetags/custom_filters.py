from django import template

register = template.Library()

@register.filter
def truncate_words(value, arg):
    words = value.split()
    if len(words) > arg:
        return ' '.join(words[:arg]) + '...'
    return value