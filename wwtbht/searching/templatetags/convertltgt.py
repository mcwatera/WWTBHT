from django import template

register = template.Library()

@register.filter
def convertltgt(value):
    value1 = value.replace("<","&lt;")
    value2 = value1.replace(">", "&gt;")
    return value2
    