import pendulum
from django import template
from django.conf import settings
from fincapes import variables
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def variable_value(name):
    return getattr(variables, name, "")


@register.simple_tag
def get_current_year(tzinfo='Asia/Jakarta'):
    today = pendulum.today(tz=tzinfo)
    return today.year
