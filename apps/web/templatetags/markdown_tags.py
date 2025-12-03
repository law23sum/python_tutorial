from copy import deepcopy

import markdown
import nh3
from django import template
from django.utils.safestring import mark_safe
from markdown.extensions.fenced_code import FencedCodeExtension

register = template.Library()


@register.filter
def render_markdown(text):
    # First convert markdown to HTML
    html = markdown.markdown(text, extensions=[FencedCodeExtension()])

    # Then sanitize the HTML with nh3
    # Allow "class" on <code> elements also
    attributes = deepcopy(nh3.ALLOWED_ATTRIBUTES)
    attributes["code"] = {"class"}
    cleaned_html = nh3.clean(html, attributes=attributes)

    # Mark as safe to avoid double-escaping
    return mark_safe(cleaned_html)
