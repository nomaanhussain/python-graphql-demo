from importlib import resources
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from requests.auth import HTTPBasicAuth
import re
import json
import requests
import yaml
from werkzeug.exceptions import HTTPException



app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    if request.method == 'GET':
        resp = jsonify("OK")
        resp.status_code = 200
        return resp
