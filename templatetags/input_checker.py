from django import template
register = template.Library()


@register.filter(name="is_select")
def is_select(field):
    return field.field.widget.__class__.__name__ == "Select"


@register.filter(name="is_checkbox")
def is_checkbox(field):
    print field.field.widget.__class__.__name__
    return field.field.widget.__class__.__name__ == "CheckboxInput"


@register.filter('is_datetime')
def is_datetime(field):
    return field.field.widget.__class__.__name__ == "DateTimeInput"
