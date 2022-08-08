from django.template import Library

register = Library()


@register.simple_tag
def get_user_rating(competency, user):
    return competency.get_user_rating(user)
