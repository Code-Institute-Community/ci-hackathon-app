import datetime
import json

from django.template import Library
from django.conf import settings

register = Library()


@register.filter
def calculate_team_level(team):
    return sum([member.get('level') for member in team])


@register.filter
def format_team_name(team_name):
    if '_' not in team_name:
        return team_name
    return ' '.join([word[0].upper() + word[1:] for word in team_name.split('_')])

@register.filter
def dump_json(teams):
    if isinstance(teams, dict):
        return json.dumps(teams)
    return teams

@register.filter
def modulo(num, val):
    return num % val == 0
