from django import template

register = template.Library()


@register.simple_tag
def get_leave_days_number(start, end):
    """
    template tag to calculate leave days
    By: amira
    date: 10/3
    """
    return (end - start).days + 1
