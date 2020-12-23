from django import template

register = template.Library()

def split(value, sep):
    return value.replace('[', '').replace(']', '').replace('\'', '').split(sep)

def length(value):
    return len(value)

def stripped(value):
    return value.strip()

register.filter('split', split)
register.filter('length', length)
register.filter('stripped', stripped)