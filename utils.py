import logging, utils, json, time, random, string, requests, datetime
from flask import jsonify

import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

# def encode_keys(entities):
#     return [dict(e.to_dict(), **dict(key=e.key.urlsafe())) for e in entities]

# def encode_key(entity):
#     logging.info('The entity fetch is : {}'.format(entity))
#     return encode_keys([entity])[0]

def dict_all_documents(documents):
    documents_dict = []
    id_number = 0
    for doc in documents:
        doc_todict = doc.to_dict()
        doc_todict['key']   = doc.key.urlsafe()
        doc_todict['id']    = id_number = id_number + 1
        documents_dict.append(doc_todict)
    return documents_dict

def dict_one_document(document_one, document_safekey):
    doc_todict          = document_one.to_dict()
    doc_todict['key']   = document_safekey
    return doc_todict

# def decode_safekey(safekey):
#     return ndb.Key(urlsafe=safekey)


# ======================== AUTHENTICATION ===================================

def apikey_generator(size=60, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


# ======================== FIREBASE ===================================

def add_log_to_firebase(log_action, log_desc):
    url = 'https://my37app.firebaseio.com/data.json'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        ""
        'log_action': log_action,
        'log_description': log_desc,
        'date_time': time.time()
    }
    response = requests.post(url, headers=headers, json=payload)
    # response_body = response.json()
    logging.info('response : {}'.format(response))
    # logging.info('response_body : {}'.format(response_body))
    return None
