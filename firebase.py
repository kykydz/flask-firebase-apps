import firebase_admin, datetime

from google.cloud import firestore
import google.cloud.exceptions

from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('my37app-2256fb803a0a.json')
firebase_admin.initialize_app(cred)


def new_collection():
    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    return db
