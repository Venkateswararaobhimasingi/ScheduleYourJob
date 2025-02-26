from django import template

register = template.Library()

@register.filter
def rangelist(value, arg):
    """Returns a range from value to arg (inclusive of value, exclusive of arg+1)."""
    return range(int(value), int(arg) + 1)

@register.filter
def get_months(_):
     return [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December")
    ]