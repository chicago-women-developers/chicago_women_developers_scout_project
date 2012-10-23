# -*- coding: utf-8 -*-
import os
from google.appengine.api import users
import webapp2
from webapp2_extras import sessions
from google.appengine.ext.webapp import template


import models
import tools.common
import settings
import logging

template.register_template_library('common.templateaddons')

class BaseRequestHandler(webapp2.RequestHandler):
  """Extension of the normal RequestHandler

  - self.userprefs provides the UserPrefs object of the current user.
  - self.render() provides a quick way to render templates with
    common template variables already preset.
  """
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    self.userprefs = models.UserPrefs.from_user(users.get_current_user())

    self.response.headers['X-UA-Compatible'] = 'chrome=1' #Make sure Google Chrome Frame gets activated

    if 'count' in self.session:
      count = int(self.session['count'])+1
    else:
      count = 0
            
    self.response.headers['X-SESSION-TEST'] = str(count)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session['count'] = count
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self.session_store.get_session()        


  def render(self, template_name, template_values={}):
    #Let's turn of GCF for those poor lost souls with IE
    self.response.headers['X-UA-Compatible'] = 'chrome=1'

    # Routes common to all templates
    nav_bar = {
      'home': webapp2.uri_for('home'),
      'login': webapp2.uri_for('login'),
      'logout': webapp2.uri_for('logout'),
      'account': webapp2.uri_for('account')
    }
    # Preset values for the template
    values = {
      'request': self.request,
      'prefs': self.userprefs,
      'login_url': users.create_login_url(self.request.uri),
      'logout_url': users.create_logout_url(self.request.uri),
      'is_testenv':tools.common.is_testenv(),
      'nav_bar': nav_bar
    }

    # Add manually supplied template values
    values.update(template_values)

    template_dir = os.path.join(os.path.dirname(__file__),
        '../%s' % webapp2.get_app().config.get('template.dir'))

    # Render template
    fn = os.path.join(template_dir, template_name)
    self.response.out.write(template.render(fn, values,
        debug=tools.common.is_testenv()))

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass        

  def error404(self):
    """Renders a standard 404 page"""
    self.render('404.html')
        
