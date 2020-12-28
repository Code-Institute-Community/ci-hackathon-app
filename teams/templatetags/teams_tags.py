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
    return team_name.split('_')[0][0].upper() + team_name.split('_')[0][1:] + ' ' + team_name.split('_')[1]


@register.filter
def dump_json(teams):
    if isinstance(teams, dict):
        return json.dumps(teams)
    return teams
