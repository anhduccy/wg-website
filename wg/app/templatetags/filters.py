from django.template.defaulttags import register

@register.filter(name='range')
def filter_range(number):
    return range(number)

@register.simple_tag
def divide(a, b):
    if a.value() is not None:
        x = int(a.value())
        return round(x/b, 2)
    return 0