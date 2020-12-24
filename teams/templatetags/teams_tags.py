from django.template import Library
import datetime
from django.conf import settings

register = Library()


@register.filter
def calculate_team_level(team):
    return sum([member.get('level') for member in team])
