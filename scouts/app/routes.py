# -*- coding: utf-8 -*-

import webapp2, handlers

# Map urls to handlers.  Keep in alphabetical order by URI.
# All handlers are in the same file, but we should consider separating them
# out when each handler does more.
urls = [
    webapp2.Route(r'/', handler=handlers.MainHandler, name="home"),
    webapp2.Route(r'/account', handler=handlers.AccountHandler, name="account"),
    webapp2.Route(r'/account_setup', handler=handlers.AccountSetupHandler, name="account_setup"),
    webapp2.Route(r'/create_event', handler=handlers.CreateEventHandler, name="create_event"),
    webapp2.Route(r'/login', handler=handlers.LoginHandler, name="login"),
    webapp2.Route(r'/login_welcome', handler=handlers.LoginWelcomeHandler, name="login_welcome"),
    webapp2.Route(r'/logout', handler=handlers.LogoutHandler, name="logout"),
    webapp2.Route(r'/scout_registration', handler=handlers.ScoutRegistrationHandler, name="scout_registration"),
    webapp2.Route(r'/user_list', handler=handlers.UserListHandler, name="user_list"),
    webapp2.Route(r'/view_event', handler=handlers.ViewEventHandler, name="view_event"),
    webapp2.Route(r'.*', handler=handlers.NotFoundHandler, name="error")
]
