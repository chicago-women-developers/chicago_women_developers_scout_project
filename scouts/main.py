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
from google.appengine.ext import db

class Event(db.Model):
    startDateTime = db.DateTimeProperty(auto_now_add=True)
    endDateTime = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    location = db.StringProperty(required=True)

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
        self.response.write("""
<form action="/createevent" method="post" id="eventform">
        <div class="form">
          <div class="field">
            <div class="name">Name</div>
            <div class="value"><input name="name" type="text" size="70"/></div>
          </div>
          <div class="field">
            <div class="name">Description</div>
            <div class="value"><input name="description" type="text" size="70"/></div>
          </div>
          <div class="buttons">
            <span class="button"><input type="submit" name="action" value="Create Event"/></span>
          </div>
        </div>
      </form>""")

    def post(self):
        # startDateTime = self.request.get('start')
        # endDateTime = self.request.get('end')
        name = self.request.get('name')
        description = self.request.get('description')
        location = "baltimore"

        event=Event(name=name,
                    description=description,
                    location=location)
        event.put()
        self.redirect('/viewevent/?name=' + name)

class ViewEventHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('view event (get)')

    def post(self):
        self.response.write('view event (post)')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/siteregistration', SiteRegistrationHandler),
    ('/scoutregistration', ScoutRegistrationHandler),
    ('/createevent', CreateEventHandler),
    ('/viewevent', ViewEventHandler)
], debug=True)
