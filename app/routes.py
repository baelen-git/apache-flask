#!flask/bin/python
from flask import Flask,request,jsonify
import requests
from os import walk
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app import app


#app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "baelen": generate_password_hash("kD48YL48vfEA")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username),
                                                 password):
        return username

download_path = '/var/www/files/'

@app.route('/api', methods=['GET'])
#@auth.login_required
def list_isos():
    print ("GET")
    filenames = next(walk(download_path), (None, None, []))[2]  # [] if no file
    return jsonify(filenames)

@app.route('/api', methods=['PUT'])
#@auth.login_required
def download_iso():
    if not request.json or not 'URL' in request.json:
        abort(400)
    print (request.json)
    URL = request.json.get('URL')
    print ("URL = " + URL)
    clusterid = request.json.get('clusterid')
    filename=download_path +  clusterid + "-discovery.iso"
    print ("Downloading " + filename)

    response = requests.get(URL)
    open(filename, "wb").write(response.content)

    return jsonify(clusterid + "-discovery.iso")

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")

