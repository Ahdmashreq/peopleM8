from django.template import Library
from django.utils.html import format_html
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error
from django import get_version

register = Library()


@register.simple_tag
def mark_as_read(slug='live_notify_list'):
    html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    return format_html(html)
