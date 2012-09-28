# -*- coding: utf-8 -*-
#
# Update the settings as needed
#

from tools.common import is_testenv

config = {}
# Configure session information here
config['webapp2_extras.sessions'] = {
    # Put your secret key in here this should be unique to each application
    'secret_key': 'put your secret key in here this should be unique to each application',
    'backend':'datastore', # See the webapp2 documentation for other options
    'cookie_name':'app-session', # set your cookie session here. You don't _have_ to call it `session`
}

config['template.dir'] = 'templates/'

config['mailchimp'] = {
    'api_key':'', # MailChimp settings to subscribe users after signup
    'list_id':'', # Find it on mailchimp.com via "settings" -> "list settings and unique id"
    
    # Use this switch to turn the MailChimp API calls on and off. Set to True only
    # for testing and production. Set to False during development.
    'enabled': False
}

config['cdn'] = {
    # If you have a CDN, set the prefix here. On the dev server nothing will be prefixed and items be served from the local dev server
    'prefix': (not is_testenv() and "http://cdn.cloudfront.net" or "")
}

