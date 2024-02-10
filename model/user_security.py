from flask import Flask, render_template, jsonify, request
from werkzeug.security import safe_str_cmp

from google.appengine.api import app_identity, urlfetch
from google.appengine.ext import ndb

import logging, utils, json
import model


class UserAccess(ndb.Model):
    username     = ndb.StringProperty()
    password     = ndb.StringProperty()
    apiKey       = ndb.StringProperty()

    @classmethod #define the ancestor root key of an entity belong to
    def root(cls):
        return  ndb.Key(cls, 'root')

    @classmethod
    def register(cls, req_json):
        logging.info('Registration user datajson is : {}'.format(req_json))
        user_access = UserAccess(parent=cls.root())
        user_access.username    = req_json['username']
        user_access.password    = req_json['password']
        user_access.apiKey      = utils.apikey_generator()
        user_access.put()
        
        user_access_dict = user_access.to_dict()
        logging.info('document is {}'.format(user_access))
        logging.info('Form of user access dictionary is : {}'.format(user_access))
        return jsonify(msg="ok", user_created=user_access_dict)

    @classmethod
    def access_key(cls, apikey_auth):
        try:
            cls.query().filter(UserAccess.apiKey==apikey_auth).fetch()[0].to_dict()
            # return True
            return jsonify(msg="ok")
        except:
            # return False
            return jsonify(msg="fail")        
    
    @classmethod
    def authenticate(cls, username, password):
        query_username = cls.query().filter(UserAccess.username==username).fetch()
        key_urlsafe = query_username[0].key.urlsafe()
        logging.info('Fetched user entity is  : {}'.format(query_username))
        logging.info('Fetched user entity URLsafe  : {}'.format(key_urlsafe))
        user = query_username[0].to_dict()
        
        logging.info('Fetched user entity user  : {}'.format(user))
        if key_urlsafe and safe_str_cmp(query_username[0].password, password):
            return key_urlsafe
        # return jsonify(msg='fetched failed')

    @classmethod
    def identity(cls, payload):
        # user_id = payload['identity']
        logging.info('Fetched user payload : {}'.format(payload))
        logging.info("---------------------------------------------")
        return userid_table.get(user_id, None)


    

