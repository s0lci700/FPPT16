from django import template

register = template.Library()


@register.filter
def filter_by_role(users, role):
    return [user for user in users if user.role == role]


@register.filter
def filter_by_year(users, year):
    return [user for user in users if user.studentprofile.year == year]
