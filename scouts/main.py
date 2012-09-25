#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
from protorpc import messages
from google.appengine.ext import db
from google.appengine.api import users

welcomeform="""
	<html>
		Welcome, %(username)s!
	</html>
"""

class User(db.Model):
    user=db.UserProperty(required=True)
    createdate = db.DateTimeProperty(auto_now_add=True)
    role=db.IntegerProperty(required=True)


class UserManager:
    def checkUserExists(self, userObj): #I have no idea why we need to pass self, but it fixes this error: checkUserExists() takes exactly 1 argument (2 given)
        userToCheck = db.GqlQuery("Select * from User where user=:1",userObj)
        if not userToCheck:
            return False
        else:
            return True

    def insertUser(user, role):
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
                self.response.out.write('User should get form to enter his/her role')
            else:
            	self.response.out.write(welcomeform % {"username":user.nickname()})
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
        self.response.write('scout register for the site (get)')

    def post(self):
        self.response.write('scout registerfor the site (post)')

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
