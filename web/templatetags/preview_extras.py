from django import template

register = template.Library()


def remove_newlines(value):
    value = value.replace("&nbsp;", "")
    value = value.replace("<p>", "")
    value = value.replace("</p>", "")
    return value

register.filter('remove_newlines', remove_newlines)
