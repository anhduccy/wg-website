from django.template.defaulttags import register
import locale

@register.filter(name='range')
def filter_range(number):
    return range(number)

@register.simple_tag
def divide(a, b):
    if a.value() is not None:
        x = int(a.value())
        return round(x/b, 2)
    return 0

@register.simple_tag
def currency(a):
    locale.setlocale(locale.LC_ALL, '')
    if a.value() is not None:
        a = float(a.value())
        return locale.currency(a, grouping=True)
    return ""