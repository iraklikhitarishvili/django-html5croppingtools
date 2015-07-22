from django import template
from django.db.models import ImageField

register = template.Library()


@register.simple_tag()
def html5crop(image_field, quality=None, dimensions=None):
    if image_field.url:
        _return = image_field.url + '?'
        _return += ('quality=' + str(quality) + '&') if quality else ''
        _return += ('dimensions=' + dimensions) if dimensions else ''
        return _return
    else:
        return ''
