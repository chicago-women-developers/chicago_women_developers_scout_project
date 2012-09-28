# -*- coding: utf-8 -*-
import logging
from google.appengine.api import memcache

# When using runtime:python27 you can just use `import json` 
from django.utils import simplejson as json # http://stackoverflow.com/questions/1171584/how-can-i-parse-json-in-google-app-engine

from google.appengine.api import urlfetch

import models


def get_someitems(clear=False):
    """Boilerplate for your customization"""
    if clear:
        memcache.delete("someitems")
        return

    someitems = memcache.get("someitems")
    if someitems:
        #logging.info("return cached someitem")
        return someitems

    someitems = []
    for someitem in Someitem.all().fetch(100):
        someitems.append(someitem)

    memcache.set("someitems", someitems)
    logging.info("cached someitems")
    return someitems


def get_userprefs(user, clear=False):
    """
    Get the UserPrefs for the current user either from memcache or, if not
    yet cached, from the datastore and put it into memcache. Used by 
    UserPrefs.from_user(user)
    """
    if not user:
        return user

    if user.federated_identity():
        key = "userprefs_fid_%s" % user.federated_identity()
    else:
        key = "userprefs_gid_%s" % user.user_id()

    # Clearing the cache does not return anything
    if clear:
        memcache.delete(key)
        logging.info("- cache cleared key: %s", key)
        return

    # Try to grab the cached UserPrefs
    prefs = memcache.get(key)
    if prefs:
        logging.info("- returning cached userprefs for key: %s", key)
        return prefs

    # If not cached, query the datastore, put into cache and return object
    prefs = models.UserPrefs._from_user(user)
    memcache.set(key, prefs)
    logging.info("cached userprefs key: %s", key)
    return prefs

def get_short_url(long_url, clear=False):
    """
    Get the short url using the public google url shortening service.
    See: http://goo.gl/ and http://code.google.com/apis/urlshortener/v1/getting_started.html
    """
    key = "short_url-%s" % long_url
    if clear:
        memcache.delete(key)
        return

    short_url = memcache.get(key)
    if short_url:
        logging.info("Return cached short url %s for %s" % (short_url, long_url))
        return short_url

    try:    
        request_data = {
            "longUrl":long_url
        }
        request_string = json.dumps(request_data)
        
        result = urlfetch.fetch(url="https://www.googleapis.com/urlshortener/v1/url",
                                payload=request_string,
                                method=urlfetch.POST,
                                headers={'Content-Type':'application/json'}
                                )    
        if result.status_code == 200:
            result_data = json.loads(result.content)
            short_url = result_data['id']
            memcache.set(key, short_url)
            logging.info("Saved to cache url %s for %s" % (short_url, long_url))
            return short_url
        raise Exception("Bad return status from url shortening service: %s" % result.status_code)
    except Exception, e:
        logging.exception(e)
    
    return None

