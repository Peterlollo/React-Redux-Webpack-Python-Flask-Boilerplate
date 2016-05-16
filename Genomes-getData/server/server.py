import requests
import flask
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
import models
import controller
from os import path
import models
import json


#Initialize Flask application
app = Flask(__name__)
PORT = 5000

#Gather data from config.py
app.config.from_object('config')

#Declaration of all necessary variables needed to perform 23AndMe API Call
API_SERVER = "api.23andme.com"
BASE_CLIENT_URL = 'http://localhost:%s/'% PORT
DEFAULT_REDIRECT_URI = '%sreceive_code/'  % BASE_CLIENT_URL
CLIENT_ID = app.config.get('CLIENT_ID')
CLIENT_SECRET = app.config.get('CLIENT_SECRET')
REDIRECT_URI = app.config.get('REDIRECT_URI')
SNPS = ["rs12913832"]
DEFAULT_SCOPE = "names basic email ancestry relatives %s" % (" ".join(SNPS))
BASE_API_URL = "https://%s/" % API_SERVER

class MyDict(dict):
    pass

@app.route('/')
def home():
    auth_url = "%sauthorize/?response_type=code&redirect_uri=%s&client_id=%s&scope=%s" % (BASE_API_URL, REDIRECT_URI, CLIENT_ID, DEFAULT_SCOPE)
    return render_template('index.html', auth_url=auth_url)

@app.route('/get_info/')
def getUser():
    print 'in the get info route=========================>>>>>>>>>>>>>>>>>>'
    rel = models.db_session.query(models.Relative).get(1)
    print 'rel ============>>>>>>>>>>>>>>>>>>>>>>', rel
    result = MyDict()
    result['name'] = str(rel.first_name)
    print 'result ===========================>>>>>>>>>>>>>>>>', result
    return jsonify(result)
   #  look into database, query for user information then return response with all of user's data

@app.route('/receive_code/')
def receive_code():
    print 'receive_code is being called'
    parameters = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': REDIRECT_URI,
        'scope': DEFAULT_SCOPE
    }
    response = requests.post(
        "%s%s" % (BASE_API_URL, "token/"),
        data = parameters,
        verify=False
    )
    #get access token from 23andMe
    if response.status_code == 200:
        access_token = response.json()['access_token']
        headers = {'Authorization': 'Bearer %s' % access_token}
        #Begin API calls to 23andMe to get all scoped user data
        genotype_response = requests.get("%s%s" % (BASE_API_URL, "1/genotype/"),
                                         params = {'locations': ' '.join(SNPS)},
                                         headers=headers,
                                         verify=False)
        user_response = requests.get("%s%s" % (BASE_API_URL, "1/user/?email=true"),
                                         headers=headers,
                                         verify=False)
        #if both API calls are successful, process user data
        if user_response.status_code == 200 and genotype_response.status_code == 200:
            user_profile_id = genotype_response.json().pop()['id']
            #if user already exists in database, render the html and do not re-add user to database
            if len(models.db_session.query(models.User).filter_by(profile_id=user_profile_id).all()) != 0:
                return flask.render_template('main.html', response_json = genotype_response.json())
            # otherwise, add new user to database if they have never logged in before
            else:
                #Begin API calls to 23andMe to get additional user data
                name_response = requests.get("%s%s" % (BASE_API_URL, "1/names/%s" % user_profile_id),
                                                 headers=headers,
                                                 verify=False)
                relatives_response = requests.get("%s%s" % (BASE_API_URL, "1/relatives/%s" % user_profile_id),
                                                   params = {'limit': 20, 'offset': 1},
                                                   headers=headers,
                                                   verify=False)
                #call createNewUser from controller to add User and User relatives to the database
                controller.createNewUser(name_response, relatives_response, genotype_response, user_response)

                return flask.render_template('main.html', response_json = genotype_response.json())
        #error handling if api calls for additional user data to 23andMe fail
        else:
            reponse_text = genotype_response.text
            response.raise_for_status()
    #error handling if initial api calls to 23andMe fail
    else:
        response.raise_for_status()


#Initialize python server on port
if __name__ == '__main__':
  print 'Server has been initialized'
  app.run(debug=True, port=PORT)
