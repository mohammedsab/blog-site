from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown_format(value):
    return markdown.markdown(value, extensions=['markdown.extensions.fenced_code'])
