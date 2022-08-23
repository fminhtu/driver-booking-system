import requests
from flask import Flask, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

# creates Flask object
app = Flask(__name__)

api_key = "AIzaSyD-HPqZ6715o4r5STSx5mGtlx8vqjTLZNc"


@app.route('/gps', methods =['POST'])
def trip_request():
    data = request.json 

    address = data.get('adress').replace(" ", "+") + "+VN"

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, api_key)
    response = requests.get(url, ploads)

    return response.json()
                

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True, port=5004)