from django.template import Library

from accounts.models import UserType

register = Library()


@register.filter
def is_type(user_type, enum_type):
    """ Checks if a user's user_type is of a specific UserType Enum """
    try:
        return user_type == UserType[enum_type]
    except KeyError:
        return


@register.filter
def is_types(user_type, enum_types_str):
    """ Checks if a user's user_type is any of a specific UserType Enum """
    try:
        enum_types = enum_types_str.split(',')
        return any([enum_type for enum_type in enum_types
                    if user_type == UserType[enum_type]])
    except KeyError:
        return
