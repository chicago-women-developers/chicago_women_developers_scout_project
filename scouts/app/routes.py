# -*- coding: utf-8 -*-

import webapp2, handlers

# Map urls to handlers.  Keep in alphabetical order by URI.
urls = [
    webapp2.Route(r'/', handler=handlers.MainHandler, name="home"),
    webapp2.Route(r'/account', handler=handlers.AccountHandler, name="account"),
    webapp2.Route(r'/account_setup', handler=handlers.AccountSetupHandler, name="account_setup"),
    webapp2.Route(r'/create_event/.*', handler=handlers.CreateEventHandler, name="create_event"),
    webapp2.Route(r'/login', handler=handlers.LoginHandler, name="login"),
    webapp2.Route(r'/logout', handler=handlers.LogoutHandler, name="logout"),
    webapp2.Route(r'/scout_registration', handler=handlers.ScoutRegistrationHandler, name="scout_registration"),
    webapp2.Route(r'/site_registration', handler=handlers.SiteRegistrationHandler, name="site_registration"),
    webapp2.Route(r'/view_event', handler=handlers.ViewEventHandler, name="view_event"),
    webapp2.Route(r'.*', handler=handlers.NotFoundHandler, name="error")
]
