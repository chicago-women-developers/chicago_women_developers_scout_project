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
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
