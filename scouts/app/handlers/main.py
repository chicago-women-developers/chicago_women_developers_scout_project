# -*- coding: utf-8 -*-
import os
import logging
import webapp2
import cgi

from hashlib import md5
from protorpc import messages
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Import packages from the project
import mc
import tools.mailchimp

from models import *
from baserequesthandler import BaseRequestHandler
from tools.common import decode
from tools.decorators import login_required, admin_required

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates/"))


registerForm="""
    <html>
        Hello, %(username)s!
        <form action="/scoutregistration" method="post">
            <input type="checkbox" name="isParent" value="true">Are you a Parent?<br>
            <input type="submit" value="Submit">
        </form>
    </html>
"""

welcomeForm="""
    <html>
        Welcome, %(username)s!
        Thank you for registering!
    </html>
"""


# Main page request handler
class Main(BaseRequestHandler):
    def get(self):
        # Render the template
        self.render("index.html")


# Account page and after-login handler
class Account(BaseRequestHandler):
    """
    The user's account and preferences. After the first login, the user is sent
    to /account?continue=<target_url> in order to finish setting up the account
    (email, username, newsletter).
    """
    def get(self):
        target_url = decode(self.request.get('continue'))
        # Circumvent a bug in gae which prepends the url again
        if target_url and "?continue=" in target_url:
            target_url = target_url[target_url.index("?continue=") + 10:]

        if not self.userprefs.is_setup:
            # First log in of user. Finish setup before forwarding.
            self.render("account_setup.html", {"target_url": target_url, 'setup_uri':self.uri_for('setup')})
            return

        elif target_url:
            # If not a new user but ?continue=<url> supplied, redirect
            self.redirect(target_url)
            return

        # Render the account website
        self.render("account.html", {'setup_uri':self.uri_for('setup')})


class AccountSetup(BaseRequestHandler):
    """Initial setup of the account, after user logs in the first time"""
    def post(self):
        username = decode(self.request.get("username"))
        email = decode(self.request.get("email"))
        subscribe = decode(self.request.get("subscribe"))
        target_url = decode(self.request.get('continue'))
        target_url = target_url or self.uri_for('account')

        # Set a flag whether newsletter subscription setting has changed
        subscription_changed = bool(self.userprefs.subscribed_to_newsletter) \
                is not bool(subscribe)

        # Update UserPrefs object
        self.userprefs.is_setup = True
        self.userprefs.nickname = username
        self.userprefs.email = email
        self.userprefs.email_md5 = md5(email.strip().lower()).hexdigest()
        self.userprefs.subscribed_to_newsletter = bool(subscribe)
        self.userprefs.put()

        # Subscribe this user to the email newsletter now (if wanted). By
        # default does not subscribe users to mailchimp in Test Environment!
        if subscription_changed and webapp2.get_app().config.get('mailchimp')['enabled']:
            if subscribe:
                tools.mailchimp.mailchimp_subscribe(email)
            else:
                tools.mailchimp.mailchimp_unsubscribe(email)

        # After updating UserPrefs, redirect
        self.redirect(target_url)

class NotFound(BaseRequestHandler):
    def get(self):
        self.error404()
        
    def post(self):
        self.error404()

class User(db.Model):
    user=db.UserProperty(required=True)
    createdate = db.DateTimeProperty(auto_now_add=True)
    role=db.IntegerProperty(required=True)


class UserManager:
    def checkUserExists(self, user): #I have no idea why we need to pass self, but it fixes this error: checkUserExists() takes exactly 1 argument (2 given)
        userToCheck = db.GqlQuery("SELECT * FROM User WHERE user = :1 ",user)
        if not userToCheck.get():
            return False
        else:
            return True

    def insertUser(self, user, role):
        userToInsert = User(user=user, role=role)
        userToInsert.put()

class Roles(messages.Enum):
    ADMIN = 1
    PARENT = 2
    SCOUT = 3

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        siteUser = UserManager()
        if user:
            userExists = siteUser.checkUserExists(user)
            if not userExists:
                self.redirect("/scoutregistration")
            else:
                self.response.out.write('Welcome ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class SiteRegistrationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('register for the site (get)')

    def post(self):
        self.response.write('registerfor the site (post)')


class ScoutRegistrationHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_values = {"username":user.nickname()}
            template = jinja_environment.get_template('registrationform.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
    def post(self):
        user = users.get_current_user()
        isParent = self.request.get('isParent')
        siteUser = UserManager()
        if isParent:
            siteUser.insertUser(user, int(Roles.PARENT))
        else:
            siteUser.insertUser(user, int(Roles.SCOUT))
        self.response.write(welcomeForm % {"username":user.nickname()})


class CreateEventHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get_all()
        self.response.write('Event is called: ' + name[0])
        
    def post(self):
        self.response.write('create event post')
        

class ViewEventHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('view event (get)')

    def post(self):
        self.response.write('view event (post)')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/siteregistration', SiteRegistrationHandler),
    ('/scoutregistration', ScoutRegistrationHandler),
    ('/createevent/.*', CreateEventHandler),
    ('/login', LoginHandler),
    ('/viewevent', ViewEventHandler)
], debug=True)