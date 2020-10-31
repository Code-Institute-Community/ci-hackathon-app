
# range snippet from: https://www.djangosnippets.org/snippets/1357/
# adjusted to current project needs based on https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
from django.template import Library

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
