import re

from math import floor

from django.forms import BaseForm
from django.forms.forms import BoundField
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.template import Context
from django.template.loader import get_template
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape

TOPCOAT_VERSION = '0.7.5'

register = template.Library()


@register.simple_tag
def topcoat_stylesheet_url(device='desktop', variant='dark', minified=True):
    """
    URL to Topcoat Stylesheet (CSS)
    """
    return '%stopcoat-%s/css/topcoat-%s-%s.%scss' % (settings.STATIC_URL, TOPCOAT_VERSION, device, variant, 'min.' if minified else '')


@register.simple_tag
def topcoat_stylesheet_tag(device='desktop', variant='dark', minified=True):
    """
    HTML tag to insert Topcoat stylesheet
    """
    if device is 'desktop':
        media = 'screen,projector'
    elif device is 'mobile':
        media = 'handheld'
    else:
        raise 'Bla'
    return u'<link rel="stylesheet" media="%s" href="%s">' % (media, topcoat_stylesheet_url(device, variant, minified))


@register.inclusion_tag('topcoat/partials/button.html')
def topcoat_button(text, **kwargs):
    """
    Render a button
    """
    button_quiet = kwargs.get('quiet', False)
    button_large = kwargs.get('large', False)
    button_cta = kwargs.get('cta', False)
    button_disabled = kwargs.get('disabled', False) and kwargs.get('enabled', True)

    # Build button classes
    button_classes = ['topcoat-button']
    if button_quiet:
        button_classes.append('topcoat-button--quiet')
    if button_large:
        button_classes.append('topcoat-button--large')
    if button_cta:
        button_classes.append('topcoat-button--cta')

    return {
        'text': text,
        'button_class': u' '.join(button_classes),
        'button_disabled': button_disabled
    }


@register.inclusion_tag('topcoat/partials/checkbox.html')
def topcoat_checkbox(text, **kwargs):
    """
    Render a button
    """
    checkbox_disabled = kwargs.get('disabled', False) and kwargs.get('enabled', True)

    return {
        'text': text,
        'checkbox_disabled': checkbox_disabled
    }


@register.inclusion_tag('topcoat/partials/icon_button.html')
def topcoat_icon_button(**kwargs):
    """
    Render a button
    """
    button_disabled = kwargs.get('disabled', False) and kwargs.get('enabled', True)

    is_quiet = kwargs.get('quiet', False)
    is_large = kwargs.get('large', False)

    button_class = 'topcoat-icon-button'
    button_class += '--large' if is_large else ''
    button_class += '--quiet' if is_quiet else ''

    icon_class = 'topcoat-icon'
    icon_class += '--large' if is_large else ''

    return {
        'button_disabled': button_disabled,
        'button_class': button_class,
        'icon_class': icon_class
    }


@register.filter
def is_disabled(field):
    """
    Returns True if fields is disabled, readonly or not marked as editable, False otherwise
    """
    if not getattr(field.field, 'editable', True):
        return True
    if getattr(field.field.widget.attrs, 'readonly', False):
        return True
    if getattr(field.field.widget.attrs, 'disabled', False):
        return True
    return False


@register.filter
def is_enabled(field):
    """
    Shortcut to return the logical negative of is_disabled
    """
    return not is_disabled(field)


@register.filter
def topcoat_input_type(field):
    """
    Return input type to use for field
    """
    try:
        widget = field.field.widget
    except:
        raise ValueError("Expected a Field, got a %s" % type(field))
    input_type = getattr(widget, 'bootstrap_input_type', None)
    if input_type:
        return unicode(input_type)
    if isinstance(widget, TextInput):
        return u'text'
    if isinstance(widget, CheckboxInput):
        return u'checkbox'
    if isinstance(widget, CheckboxSelectMultiple):
        return u'multicheckbox'
    if isinstance(widget, RadioSelect):
        return u'radioset'
    return u'default'


@register.simple_tag
def active_url(request, url, output=u'active'):
    # Tag that outputs text if the given url is active for the request
    if url == request.path:
        return output
    return ''


@register.filter
def split(text, splitter):
    """
    Split a string
    """
    return text.split(splitter)


@register.filter
def html_attrs(attrs):
    """
    Display the attributes given as html attributes :
    >>> import collections
    >>> html_attrs(collections.OrderedDict([('href',"http://theurl.com/img.png"), ('alt','hi "guy')]))
    u'href="http://theurl.com/img.png" alt="hi &quot;guy" '
    """
    pairs = []
    for name, value in attrs.items():
        pairs.append(u'%s="%s"' % (escape(name), escape(value)))
    return mark_safe(u' '.join(pairs))




@register.inclusion_tag("bootstrap_toolkit/icon.html")
def bootstrap_icon(icon, **kwargs):
    """
    Render an icon
    """
    icon_class = 'icon-' + icon
    if kwargs.get('inverse'):
        icon_class += ' icon-white'
    return {
        'icon_class': icon_class,
    }

