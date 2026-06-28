from django import template

register = template.Library()

@register.filter
def indian_currency(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    s = str(value)[::-1]
    groups = []

    # First group of 3 digits
    groups.append(s[:3])
    s = s[3:]

    # Then groups of 2 digits
    while s:
        groups.append(s[:2])
        s = s[2:]

    return ','.join(groups)[::-1]
