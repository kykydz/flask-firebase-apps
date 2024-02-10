from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from flask_basicauth import BasicAuth

# from firebase import new_collection

from model import Document
import logging

__author__  = "Rizky"
__version__ = "2018-10-21"
__status__  = "test"


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mvwC1N4X5Ap4Q4GZqiJ7'
app.jinja_env.line_statement_prefix = '#'
app.jinja_env.line_comment_prefix = '##'

app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
basic_auth = BasicAuth(app)

# Uncomment if you want to protect entire endpoint
# app.config['BASIC_AUTH_FORCE'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/documents/logs', methods=['GET'])
def list_documents_logs():
    return render_template('document_logs.html')

@app.route('/documents')
def list_documents():
    return jsonify(data=Document.get_all()), 200


@app.route('/documents/<document_safekey>')
def get_document(document_safekey):
    return jsonify(data=Document.get_one(document_safekey) )


@app.route('/documents', methods=['POST'])
@basic_auth.required
def create_document():
    return jsonify(data= Document.create( request.get_json() ) ), 200


@app.route('/documents/<document_safekey>', methods=['PUT'])
@basic_auth.required
def update_document(document_safekey):
    return jsonify(data = Document.update(document_safekey, request.get_json()) ), 200


@app.route('/documents/<document_safekey>/dps_score', methods=['PUT'])
@basic_auth.required
def update_document_dps_score(document_safekey):
    return jsonify(data = Document.update_dps_score(document_safekey, request.get_json()) ), 200


@app.route('/documents/<document_safekey>', methods=['DELETE'])
@basic_auth.required
def delete_document(document_safekey):
    return jsonify(data = Document.remove(document_safekey) ), 200


## ==========================================  User Route  ============================================


@app.route('/user/register', methods=['POST'])
def create_user():
    return AccountModel.register(request.get_json())

# =========================================== Fire Base ===============================================

