
# range snippet from: https://www.djangosnippets.org/snippets/1357/
# adjusted to current project needs based on https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
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
