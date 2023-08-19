from django import template

register = template.Library()


@register.filter
def filter_by_role(users, role):
    return [user for user in users if user.role == role]
