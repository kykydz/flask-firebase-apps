from flask import Flask, render_template, jsonify, request
from werkzeug.security import safe_str_cmp

from google.appengine.api import app_identity, urlfetch
from google.appengine.ext import ndb

import logging, utils, json, string, random
import model


class User(ndb.Model):
    username     = ndb.StringProperty()
    password     = ndb.StringProperty()
    api_key      = ndb.StringProperty()

    @classmethod #define the ancestor root key of an entity belong to
    def root(cls):
        return  ndb.Key(cls, 'root')

    @classmethod
    def register(cls, req_json):
        logging.info('Registering a new User..')
        
        new_user = User(parent=cls.root())
        
        new_user.username    = req_json['username']
        new_user.password    = req_json['password']
        new_user.api_key     = ''.join(random.choice(string.ascii_lowercase) for i in range(20))

        new_user.put()
        
        logging.info('User: {}'.format(new_user.to_dict()))

        return jsonify(msg="ok", user=new_user.to_dict())

    @classmethod
    def is_key_valid(cls, json_req_api_key):
        return cls.query().filter(cls.api_key==json_req_api_key).get() is not None