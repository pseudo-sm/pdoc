from django import template

register = template.Library()

@register.filter(name='replace_filter')
def replace_filter(string):
    to = " "
    by = "-"
    return string.replace(to,by)

@register.filter(name='trim')
def trim(string):
    print(string)
    return string[100:]
