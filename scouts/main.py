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
    ('/viewevent', ViewEventHandler)
], debug=True)
