from django.template import Library

register = Library()


@register.filter
def readable_user_type(user_type):
    return str(user_type).split('.')[-1]


@register.filter
def readable_lms_module(lms_module):
    return ' '.join(lms_module.split('_'))


@register.simple_tag
def split_string(**kwargs):
    string = kwargs['string']
    delimiter = kwargs['delimiter']
    index = kwargs['index']
    return string.split(delimiter)[index]
