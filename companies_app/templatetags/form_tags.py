"""
This module defines custom template filters for use in Django templates.

Functions:
    - add_class(value, arg): Adds a CSS class to a form field widget.
"""
from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(form_field, arg):
    """
    Add a CSS class to a form field widget.

    Args:
        form_field: The form field to which the class should be added.
        arg (str): The CSS class to add to the form field.

    Returns:
        The form field with the added CSS class.
    """
    return form_field.as_widget(attrs={'class': arg})
