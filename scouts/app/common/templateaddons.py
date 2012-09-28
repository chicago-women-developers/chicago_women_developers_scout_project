# -*- coding: utf-8 -*-
from google.appengine.ext.webapp import template
from django.template import Node
from mc import cache
import webapp2
"""
Custom template tags, for use from within the templates.

Before rendering a relevant template from within a handler, you need to include
the custom tags with this line of code:

    template.register_template_library('common.templateaddons')

More infos about custom template tags:

- http://docs.djangoproject.com/en/dev/howto/custom-template-tags/
"""

# get registry, we need it to register our filter later.
register = template.create_template_register()


def truncate_chars(value, maxlen):
    """Truncates value and appends '...' if longer than maxlen.
    Usage inside template to limit my_var to 20 characters max:

        {{ my_var|truncate_chars:20 }}

    """
    if len(value) < maxlen:
        return value
    else:
        return "%s..." % value[:maxlen - 3]

register.filter(truncate_chars)

def short_url(long_url):
    """Returns the short url as used by the public google url shortening service
    See: http://goo.gl/ and http://code.google.com/apis/urlshortener/v1/getting_started.html
    """
    return cache.get_short_url(long_url)
    
register.filter(short_url)

def prefix_cdn(value):
    """Simply prefixes the string with what is in settings.CDN_PREFIX. Use when
    locating resources, eg: <img src="{{"/img/myimage.jpg"|prefix_cdn}}"/>
    """
    
    app = webapp2.get_app()
    cdn_config = app.config.get('cdn')
    prefix = cdn_config['prefix']
    
    if not value:
        return None
    
    return "%s%s" % (prefix, value)

register.filter(prefix_cdn)
