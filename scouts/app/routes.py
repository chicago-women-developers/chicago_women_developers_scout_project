# -*- coding: utf-8 -*-

import webapp2, handlers

# Map url's to handlers
urls = [
    webapp2.Route(r'/', handler=handlers.Main, name="home"),
    webapp2.Route(r'/siteregistration', handler=handlers.SiteRegistrationHandler, name="siteregistration"),
    webapp2.Route(r'/scoutregistration', handler=handlers.ScoutRegistrationHandler, name="scoutregistration"),
    webapp2.Route(r'/createevent/.*', handler=handlers.CreateEventHandler, name="createeventhandler"),
    webapp2.Route(r'/login', handler=handlers.LoginHandler, name="login"),
    (r'.*', handlers.NotFound)
]
