
# range snippet from: https://www.djangosnippets.org/snippets/1357/
# adjusted to current project needs based on https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
from operator import itemgetter

from django.template import Library
import datetime
from django.conf import settings

register = Library()


@register.filter
def get_range(value, start):
    """
        Filter - returns a list containing range made from given value
        Usage (in template):
        <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
        {% endfor %}</ul>
        Results with the HTML:
        <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
        </ul>
        Instead of 3 one may use the variable set in the views
    """
    return range(start, value+1, 1)


@register.filter
def event_ended(date_event):
    '''Set a filter to check if hackaton has ended
    In order to show the enroll button only for hackatons which are not ended
    Date can be updated if organisers want to put a deadline to enrol
    Help provided in Stack overflow: https://stackoverflow.com/questions/64605335/comparing-dates-using-a-comparator-inside-django-template/64605785#64605785'''
    return date_event.date() >= datetime.date.today()


@register.filter
def get_value_from_dict(data, key):
    """ Retrieves a value from a dict based on a given key """
    if key:
        return data.get(key)


@register.filter
def to_list(data):
    return list(data)


@register.filter
def sort_list(data):
    return sorted(list(data))


@register.filter
def place_identifier(num):
    num_str = str(num)
    if not isinstance(num, int):
        # no score
        return ''
    if num_str[-1] == '1':
        return num_str + 'st'
    elif num_str[-1] == '2':
        return num_str + 'nd'
    elif num_str[-1] == '3':
        return num_str + 'rd'
    else:
        return num_str + 'th'