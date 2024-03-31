from django.template.defaulttags import register

@register.filter(name='range')
def filter_range(number):
    return range(number)