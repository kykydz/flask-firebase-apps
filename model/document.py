from google.appengine.api import app_identity, urlfetch
from google.appengine.ext import ndb

import logging, utils, json, time
import model


class Document(ndb.Model):
    
    doctype     = ndb.StringProperty()
    country     = ndb.StringProperty()
    mrz         = ndb.StringProperty()
    alphahash   = ndb.StringProperty()
    picture     = ndb.TextProperty()
    dps_score   = ndb.IntegerProperty()
    

    def get_dps_score(self): 
        logging.info('Computing DPS score')
        try:
            self.dps_score = int( model.ApiIgloo.get_dps_score(doc_mrz=self.mrz, doc_picture=self.picture.split(',')[1]) )
            logging.info('DPS score: {}'.format(self.dps_score))                                      
        except Exception as e:
            logging.error('Error, DPS score cannot be computed {}'.format(e))
            self.dps_score = -1
        return self.dps_score


    @classmethod #define the ancestor root key of an entity belong to
    def root(cls):
        return  ndb.Key(cls, 'root')


    @classmethod
    def get_all(cls):
        log_action = "GET"
        log_msg = "Fetching all entities of kind Document from datastore"
        logging.info(log_msg)
        log_firebase = utils.add_log_to_firebase(log_action, log_msg)
        documents = cls.query(ancestor=cls.root()).filter().fetch()
        # return utils.encode_keys(documents)
        return utils.dict_all_documents(documents)

    @classmethod
    def get_one(cls, document_safekey):
        logging.info('Fetching the entity of kind Document from datastore with ID {}'.format(document_safekey))
        document = ndb.Key(urlsafe=document_safekey).get()
        # document = cls.query(ancestor=cls.root()).filter('Key'=document_safekey).fetch()
        logging.info('-----------'*5)
        logging.info('Document ndb get Alphahash value {}'.format(document.alphahash))
        # return utils.encode_key(document)
        return utils.dict_one_document(document, document_safekey)

    @classmethod
    def create(cls, json_request):
        document = Document(parent=cls.root())
        logging.info('Document in json request doctype is : {}'.format(type(document)))
        document.doctype    = json_request['doctype']
        document.country    = json_request['country']
        document.mrz        = json_request['mrz']
        document.alphahash  = json_request['alphahash']
        document.picture    = json_request['picture']
        document.get_dps_score()

        logging.info('Creating on new entity of kind Document with MRZ {}'.format(document.mrz))
        document_key = document.put()

        return document.get_one(document_key.urlsafe())


    @classmethod
    def update(cls, document_safekey, json_request):
        
        document = ndb.Key(urlsafe=document_safekey).get()
        logging.info('Document in json request doctype is : {}'.format(type(document)))
        if json_request is not None:
            document.doctype    = json_request['doctype']
            document.country    = json_request['country']
            document.mrz        = json_request['mrz']
            document.alphahash  = json_request['alphahash']
            document.picture    = json_request['picture']

        document.get_dps_score()
        logging.info('Updating an entity of kind Document with MRZ {}'.format(document.mrz))
        document_key = document.put()

        return document.get_one(document_key.urlsafe())

    @classmethod
    def update_dps_score(self, document_safekey, json_request):
        return Document.update(document_safekey, json_request=None)


    @classmethod
    def remove(cls, document_safekey):
        # document = Document(parent=cls.root())
        logging.info('Document safe key obtained is : {}'.format(document_safekey))
        document_key = ndb.Key(urlsafe=document_safekey).get()
        document_key.key.delete()
        return ("Document Deleted")