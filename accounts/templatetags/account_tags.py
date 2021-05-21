from django.template import Library

from accounts.models import UserType

register = Library()


@register.filter
def is_type(user_type, enum_type):
    try:
        return user_type == UserType[enum_type]
    except KeyError:
        return
